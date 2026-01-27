from ultralytics import YOLO

model = YOLO("yolov8s_custom.pt")

model.predict(source=0, show = True,  conf=0.5 , line_thickness=1)