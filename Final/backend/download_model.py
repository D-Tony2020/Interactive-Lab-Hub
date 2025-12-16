import torch
# Patch for PyTorch 2.6+
_original_load = torch.load
def _safe_load_wrapper(*args, **kwargs):
    if 'weights_only' not in kwargs: kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _safe_load_wrapper

from ultralytics import YOLO
import os

print("Downloading yolov8n.pt...")
try:
    model = YOLO("yolov8n.pt")
    print("Standard YOLO loaded successfully!")
except Exception as e:
    print(f"Error loading standard YOLO: {e}")

print("Downloading YOLOv8s-world.pt...")
try:
    model = YOLO("yolov8s-world.pt")
    print("YOLO-World loaded successfully!")
    print(f"Model path: {os.path.abspath('yolov8s-world.pt')}")
except Exception as e:
    print(f"Error loading YOLO-World: {e}")
