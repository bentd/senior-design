import cv2
import numpy as np
import onnxruntime as ort
import torch
import matplotlib.pyplot as plt

# === CONFIG ===
class_names = ["person", "cup", "ball", "pen", "pencil"]
CONF_THRESHOLD = 0.1
INPUT_SIZE = 640
MAX_BOXES = 2
model_path = "../models/quant_yolotiny.onnx"

# === LOAD MODEL ===
session = ort.InferenceSession(model_path)
input_name = session.get_inputs()[0].name

# === START WEBCAM ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Webcam not found.")
    exit()

plt.ion()
fig, ax = plt.subplots()
fig.canvas.manager.set_window_title("YOLO Tiny - Live Detection")

print("📷 Running. Close the window to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_resized = cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    img_input = frame_rgb / 255.0
    img_input = np.transpose(img_input, (2, 0, 1))
    img_input = np.expand_dims(img_input, axis=0).astype(np.float32)

    # Inference
    output = session.run(None, {input_name: img_input})
    output_tensor = torch.tensor(output[0]).view(MAX_BOXES, 5 + len(class_names))
    print("Raw ONNX Output:")
    print(output_tensor)

    for box in output_tensor:
        x, y, w, h, conf = box[:5]
        if conf > CONF_THRESHOLD:
            class_scores = box[5:]
            class_id = int(torch.argmax(class_scores))
            label = class_names[class_id]
            score = class_scores[class_id].item()

            # Clamp x, y, w, h between 0 and 1
            x = torch.clamp(x, 0, 1).item()
            y = torch.clamp(y, 0, 1).item()
            w = torch.clamp(w, 0, 1).item()
            h = torch.clamp(h, 0, 1).item()

            xc, yc = int(x * INPUT_SIZE), int(y * INPUT_SIZE)
            ww, hh = int(w * INPUT_SIZE), int(h * INPUT_SIZE)
            x1, y1 = max(0, xc - ww // 2), max(0, yc - hh // 2)
            x2, y2 = min(INPUT_SIZE, xc + ww // 2), min(INPUT_SIZE, yc + hh // 2)

            cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame_rgb, f"{label} {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    ax.clear()
    ax.imshow(frame_rgb)
    ax.set_axis_off()
    plt.pause(0.001)

cap.release()
plt.close()
