import os
import cv2
import torch
import onnxruntime as ort
import numpy as np

# === CONFIG ===
IMAGE_DIR = "data/images/val"
LABEL_DIR = "data/labels/val"
ONNX_PATH = "models/quant_yolotiny.onnx"
OUTPUT_DIR = "eval_output"
CONF_THRESHOLD = 0.01
NUM_CLASSES = 5
MAX_BOXES = 2
CLASS_NAMES = ["ball", "cup", "pen", "pencil", "person"]

os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess(img):
    img_resized = cv2.resize(img, (640, 640))  # Resize for inference only
    img_normalized = img_resized / 255.0
    img_transposed = np.transpose(img_normalized, (2, 0, 1)).astype(np.float32)
    return np.expand_dims(img_transposed, axis=0)

def load_labels(label_path, img_w, img_h):
    boxes = []
    if not os.path.exists(label_path):
        return boxes
    with open(label_path, 'r') as f:
        for line in f:
            cls, x, y, w, h = map(float, line.strip().split())
            x1 = int((x - w/2) * img_w)
            y1 = int((y - h/2) * img_h)
            x2 = int((x + w/2) * img_w)
            y2 = int((y + h/2) * img_h)
            boxes.append((int(cls), x1, y1, x2, y2))
    return boxes

ort_session = ort.InferenceSession(ONNX_PATH)

for img_name in os.listdir(IMAGE_DIR):
    if not img_name.endswith((".jpg", ".jpeg", ".png")):
        continue

    img_path = os.path.join(IMAGE_DIR, img_name)
    label_path = os.path.join(LABEL_DIR, os.path.splitext(img_name)[0] + ".txt")
    image = cv2.imread(img_path)
    img_h, img_w = image.shape[:2]

    input_tensor = preprocess(image)
    outputs = ort_session.run(None, {"input": input_tensor})[0]
    outputs = torch.tensor(outputs).view(MAX_BOXES, 5 + NUM_CLASSES)

    for box in outputs:
        x, y, w, h, conf = box[:5]
        scores = box[5:]
        class_id = torch.argmax(scores).item()
        prob = torch.softmax(scores, dim=0)[class_id].item()
        if conf * prob < CONF_THRESHOLD:
            continue

        x = torch.clamp(x, 0, 1).item()
        y = torch.clamp(y, 0, 1).item()
        w = torch.clamp(w, 0, 1).item()
        h = torch.clamp(h, 0, 1).item()

        x1 = int((x - w/2) * img_w)
        y1 = int((y - h/2) * img_h)
        x2 = int((x + w/2) * img_w)
        y2 = int((y + h/2) * img_h)

        label = f"{CLASS_NAMES[class_id]} ({conf*prob:.2f})"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    gt_boxes = load_labels(label_path, img_w, img_h)
    for cls, x1, y1, x2, y2 in gt_boxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(image, f"GT: {CLASS_NAMES[cls]}", (x1, y2 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    out_path = os.path.join(OUTPUT_DIR, img_name)
    cv2.imwrite(out_path, image)

print("✅ Done: Saved annotated images to eval_output/")
