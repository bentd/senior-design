import torch
from ultralytics import YOLO

model = YOLO("yolov8s_custom.pt")

torch_model = model.model
torch.save(torch_model, 'torch_model.pth')