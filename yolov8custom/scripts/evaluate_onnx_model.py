import os
import cv2
import torch
import onnxruntime as ort
import numpy as np
from sklearn.metrics import f1_score, roc_auc_score, precision_recall_curve, auc

IMAGE_DIR = "data/images/val"
LABEL_DIR = "data/labels/val"
ONNX_PATH = "models/quant_yolotiny.onnx"
CONF_THRESHOLD = 0.01
NUM_CLASSES = 5
MAX_BOXES = 2
IOU_THRESHOLD = 0.5

def compute_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2]-box1[0]) * (box1[3]-box1[1])
    box2_area = (box2[2]-box2[0]) * (box2[3]-box2[1])
    return inter_area / (box1_area + box2_area - inter_area + 1e-6)

def preprocess(img):
    img_resized = cv2.resize(img, (640, 640))
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
            x1 = (x - w/2) * img_w
            y1 = (y - h/2) * img_h
            x2 = (x + w/2) * img_w
            y2 = (y + h/2) * img_h
            boxes.append((int(cls), x1, y1, x2, y2))
    return boxes

ort_session = ort.InferenceSession(ONNX_PATH)
y_true, y_pred, y_scores = [], [], []

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

        x1 = (x - w/2) * img_w
        y1 = (y - h/2) * img_h
        x2 = (x + w/2) * img_w
        y2 = (y + h/2) * img_h
        pred_box = (class_id, x1, y1, x2, y2)

        gt_boxes = load_labels(label_path, img_w, img_h)
        matched = False
        for gt in gt_boxes:
            if class_id == gt[0] and compute_iou(pred_box[1:], gt[1:]) > IOU_THRESHOLD:
                y_true.append(1)
                matched = True
                break
        if not matched:
            y_true.append(0)
        y_scores.append(prob)
        y_pred.append(1)

if y_true:
    f1 = f1_score(y_true, y_pred)
    auroc = roc_auc_score(y_true, y_scores)
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    aupr = auc(recall, precision)

    print(f"✅ F1 Score: {f1:.4f}")
    print(f"✅ AU-ROC: {auroc:.4f}")
    print(f"✅ AU-PR: {aupr:.4f}")
else:
    print("⚠️ No valid predictions — try lowering CONF_THRESHOLD or retraining.")
