from ultralytics import YOLO
import os

print(f"CWD: {os.getcwd()}")
print("Checking for yolo11l.pt...")
if os.path.exists("yolo11l.pt"):
    print(f"File exists. Size: {os.path.getsize('yolo11l.pt')} bytes")
else:
    print("File DOES NOT exist.")

try:
    print("Loading model...")
    model = YOLO('yolo11l.pt')
    print("Model loaded successfully.")
    print(model.info())
except Exception as e:
    print(f"Error loading model: {e}")
