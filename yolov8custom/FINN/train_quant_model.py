import os
import glob
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
from brevitas.export import export_qonnx

from quantized_yolo_tiny import QuantizedYOLOTiny

# === CONFIG ===
IMAGE_DIR = "../data/images/train"
LABEL_DIR = "../data/labels/train"
NUM_CLASSES = 5
NUM_BOXES = 3
BATCH_SIZE = 8
EPOCHS = 1
IMAGE_SIZE = 640
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

torch.manual_seed(42)
if DEVICE == "cuda":
    torch.cuda.manual_seed(42)
torch.backends.cudnn.benchmark = False
torch.set_float32_matmul_precision('high')

# === TRANSFORMS ===
transform = A.Compose([
    A.Resize(IMAGE_SIZE, IMAGE_SIZE),
    A.Normalize(),
    ToTensorV2()
])

# === DATASET ===
class YoloDetectionDataset(Dataset):
    def __init__(self, image_dir, label_dir, transform=None):
        self.image_paths = []
        self.label_paths = []
        self.transform = transform

        all_images = glob.glob(os.path.join(image_dir, "*.jpg")) + \
                     glob.glob(os.path.join(image_dir, "*.jpeg")) + \
                     glob.glob(os.path.join(image_dir, "*.png"))

        for img_path in sorted(all_images):
            base = os.path.splitext(os.path.basename(img_path))[0]
            label_path = os.path.join(label_dir, base + ".txt")
            if os.path.exists(label_path):
                self.image_paths.append(img_path)
                self.label_paths.append(label_path)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label_path = self.label_paths[idx]

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = []
        with open(label_path, 'r') as f:
            for line in f.readlines():
                cls, x, y, w, h = map(float, line.strip().split())
                boxes.append([cls, x, y, w, h])

        if self.transform:
            transformed = self.transform(image=image)
            image = transformed['image']

        target = torch.zeros((NUM_BOXES, 6))
        for i, box in enumerate(boxes[:NUM_BOXES]):
            target[i, :5] = torch.tensor(box)
            target[i, 5] = 1  # object mask

        return image, target

# === LOSS FUNCTION ===
def yolo_loss(preds, targets, num_classes):
    pred_box = preds[:, :, 0:4]
    pred_obj = preds[:, :, 4]
    pred_cls = preds[:, :, 5:]

    target_cls = targets[:, :, 0].long()
    target_box = targets[:, :, 1:5]
    obj_mask = targets[:, :, 5]

    loc_loss = nn.MSELoss(reduction='none')(pred_box, target_box)
    loc_loss = (loc_loss.sum(dim=-1) * obj_mask).mean()

    obj_loss = nn.BCEWithLogitsLoss()(pred_obj, obj_mask)

    class_loss = nn.CrossEntropyLoss(reduction='none')(
        pred_cls.permute(0, 2, 1),
        target_cls
    )
    class_loss = (class_loss * obj_mask).mean()

    return loc_loss + obj_loss + class_loss

# === INIT MODEL ===
model = QuantizedYOLOTiny(num_classes=NUM_CLASSES, num_boxes=NUM_BOXES).to(DEVICE)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

dataset = YoloDetectionDataset(IMAGE_DIR, LABEL_DIR, transform)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# === TRAIN LOOP ===
history = []
print("🚀 Starting training...")

for epoch in range(EPOCHS):
    model.train()
    epoch_loss = 0.0
    total_time = 0.0
    total_images = 0

    for imgs, targets in loader:
        imgs, targets = imgs.to(DEVICE), targets.to(DEVICE)

        start = time.time()
        preds = model(imgs).view(-1, NUM_BOXES, 5 + NUM_CLASSES)
        loss = yolo_loss(preds, targets, num_classes=NUM_CLASSES)
        end = time.time()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_time += (end - start)
        total_images += imgs.size(0)
        epoch_loss += loss.item()

    avg_loss = epoch_loss / len(loader)
    mttd = total_time / total_images if total_images > 0 else 0

    print(f"Epoch {epoch + 1}/{EPOCHS} - Loss: {avg_loss:.4f} - MTTD: {mttd:.4f}s")
    history.append({"epoch": epoch + 1, "loss": avg_loss, "mttd": mttd})

# === FREEZE QUANTIZERS ===
for module in model.modules():
    if hasattr(module, 'quant_weight_enabled'):
        module.quant_weight_enabled = False
    if hasattr(module, 'quant_act_enabled'):
        module.quant_act_enabled = False

# === SAVE TRAINED MODEL ===
os.makedirs("../models", exist_ok=True)
torch.save(model.state_dict(), "../models/quant_yolotiny_trained.pth")
print("✅ Model saved to ../models/quant_yolotiny_trained.pth")

# === SAVE METRICS ===
os.makedirs("../metrics", exist_ok=True)
df = pd.DataFrame(history)
df.to_csv("../metrics/training_metrics.csv", index=False)
print("📊 Metrics saved to ../metrics/training_metrics.csv")

# === PLOT LOSS CURVE ===
plt.plot(df["epoch"], df["loss"], label="Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss Over Epochs")
plt.grid(True)
plt.legend()
plt.savefig("../metrics/loss_curve.png")
print("📉 Loss curve saved to ../metrics/loss_curve.png")



# === EXPORT TO QONNX ===
model.eval()
dummy_input = torch.randn(1, 3, IMAGE_SIZE, IMAGE_SIZE).to(DEVICE)

export_qonnx(
    model,
    dummy_input,
    export_path="../models/quant_yolotiny_qonnx.onnx"
)

print("🧠 Exported QONNX model to ../models/quant_yolotiny_qonnx.onnx")
