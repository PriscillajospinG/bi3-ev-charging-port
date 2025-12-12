import cv2
import os
from ultralytics import YOLO
from datetime import datetime, timedelta

def test_process(file_path):
    print(f"Testing processing for {file_path}")
    if not os.path.exists(file_path):
        print("File not found")
        return

    try:
        print("Loading model...")
        model = YOLO('yolo11l.pt')
        print("Model loaded.")

        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("ERROR: Failed to open video file")
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Video opened. FPS: {fps}")
        
        frame_count = 0
        max_frames = 30 # Just test first 30 frames
        
        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % 10 == 0:
                print(f"Processing frame {frame_count}...")
                results = model(frame, verbose=False)
                print(f"  Results: {len(results[0].boxes)} boxes")

        print("Finished test processing loop.")
        cap.release()
        
    except Exception as e:
        print(f"Exception during test: {e}")

if __name__ == "__main__":
    # Use one of the existing files
    target = "temp_uploads/70c8b97a-7f48-4cdd-b650-63530fba2a6d_WhatsApp Video 2025-12-11 at 22.43.12.mp4"
    test_process(target)
