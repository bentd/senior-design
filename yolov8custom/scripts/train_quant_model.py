import os
import glob
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2

from quantized_yolo_tiny import QuantizedYOLOTiny

# === CONFIG ===
IMAGE_DIR = "../data/images/train"
LABEL_DIR = "../data/labels/train"
NUM_CLASSES = 5
NUM_BOXES = 2
BATCH_SIZE = 8
EPOCHS = 25
IMAGE_SIZE = 640
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# === TRANSFORMS ===
transform = A.Compose([
    A.Resize(IMAGE_SIZE, IMAGE_SIZE),
    A.Normalize(),
    ToTensorV2()
])

# === DATASET CLASS ===
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
            target[i, 5] = 1

        return image, target

# === INIT ===
model = QuantizedYOLOTiny(num_classes=NUM_CLASSES, num_boxes=NUM_BOXES).to(DEVICE)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

dataset = YoloDetectionDataset(IMAGE_DIR, LABEL_DIR, transform)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# === TRAINING LOOP ===
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

        preds = model(imgs)
        preds = preds.view(-1, NUM_BOXES, 5 + NUM_CLASSES)

        loss = criterion(preds[:, :, :5], targets[:, :, :5])

        end = time.time()
        total_time += (end - start)
        total_images += imgs.size(0)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    avg_loss = epoch_loss / len(loader)
    mttd = total_time / total_images if total_images > 0 else 0

    print(f"Epoch {epoch + 1}/{EPOCHS} - Loss: {avg_loss:.4f} - MTTD: {mttd:.4f}s")

    history.append({
        "epoch": epoch + 1,
        "loss": avg_loss,
        "mttd": mttd
    })

# === SAVE TRAINED MODEL ===
os.makedirs("../models", exist_ok=True)
torch.save(model.state_dict(), "../models/quant_yolotiny_trained.pth")
print("✅ Model saved to ../models/quant_yolotiny_trained.pth")

# === SAVE METRICS CSV ===
os.makedirs("../metrics", exist_ok=True)
df = pd.DataFrame(history)
df.to_csv("../metrics/training_metrics.csv", index=False)
print("📊 Metrics saved to ../metrics/training_metrics.csv")
