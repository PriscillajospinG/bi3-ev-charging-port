import cv2
import os
import asyncio
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from ultralytics import YOLO

from ..database import AsyncSessionLocal
from ..models.events import VehicleEvent

# Global model instance to avoid reloading
_model = None

def get_yolo_model():
    global _model
    if _model is None:
        print("Loading YOLOv11 model...")
        # Assuming yolo11l.pt exists in current dir or downloaded
        # If not, ultralytics will download it
        _model = YOLO('yolo11l.pt')
    return _model

async def process_video_file(file_path: str, filename: str):
    """
    Background Task: Process video -> YOLO detection -> DB Insert
    """
    print(f"Starting processing for {filename}...")
    print(f"File path: {os.path.abspath(file_path)}")
    
    try:
        model = get_yolo_model()
        print("Model retrieved.")
        
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print(f"ERROR: Could not open video file: {file_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        print(f"Video opened. FPS: {fps}")
        frame_interval = int(fps) # Process 1 frame per second to save resources
        
        events_to_save = []
        frame_count = 0
        
        # We start "timestamp" at now, and increment by video time
        start_time = datetime.now()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            if frame_count % frame_interval != 0:
                continue
                
            # Run Inference
            results = model(frame, verbose=False)
            
            # Analyze results
            detected_objects = []
            if results and results[0].boxes:
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]
                    conf = float(box.conf[0])
                    
                    # Filter for vehicles
                    if class_name in ['car', 'truck', 'bus', 'motorcycle'] and conf > 0.5:
                        detected_objects.append((class_name, conf))
            
            # Create events for this second
            current_video_time = start_time + timedelta(seconds=frame_count/fps)
            
            # To avoid spamming DB, let's just save valid detections
            for obj_class, obj_conf in detected_objects:
                events_to_save.append(
                    VehicleEvent(
                        timestamp=current_video_time,
                        video_source=filename,
                        class_name=obj_class,
                        confidence=obj_conf,
                        event_type='detection'
                    )
                )

        cap.release()
        
        # Bulk Insert
        if events_to_save:
            print(f"Saving {len(events_to_save)} detection events to DB...")
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    session.add_all(events_to_save)
            print(f"Processing complete for {filename}.")
        else:
            print(f"No vehicles detected in {filename}.")
            
    except Exception as e:
        print(f"Error processing video {filename}: {e}")
    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)
