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
        # Assuming yolo11n.pt (Nano) exists or downloaded. Lighter and faster.
        _model = YOLO('yolo11n.pt')
    return _model

async def process_video_file(file_path: str, filename: str):
    """
    Background Task: Process video -> YOLO detection -> Draw Boxes -> Save to Static -> DB Insert
    """
    print(f"Starting processing for {filename}...")
    print(f"File path: {os.path.abspath(file_path)}")
    
    output_filename = f"processed_{filename}"
    output_dir = "static/videos"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        model = get_yolo_model()
        print("Model retrieved.")
        
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print(f"ERROR: Could not open video file: {file_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Video opened. FPS: {fps}, Resolution: {width}x{height}")
        
        # Initialize Video Writer
        # 'avc1' is H.264, widely supported by browsers. 
        # If this fails in the container, we might need 'vp09' (WebM) or ensure libx264 is present.
        # But let's try avc1 first as it's standard for .mp4
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_interval = int(fps) # Process 1 frame per second for DB events, but write ALL frames for video
        
        events_to_save = []
        frame_count = 0
        
        # We start "timestamp" at now, and increment by video time
        start_time = datetime.now()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Run Inference on every frames (or every Nth frame and track?)
            # For smooth video, we should infer every frame or persist detections.
            # To save compute, we might infer every 5th frame. 
            # For this MVP, let's infer every frame to look good.
            results = model(frame, verbose=False)
            
            # Draw Detections
            if results and results[0].boxes:
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]
                    conf = float(box.conf[0])
                    
                    if class_name in ['car', 'truck', 'bus', 'motorcycle'] and conf > 0.5:
                        # Draw Box
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f"{class_name} {conf:.2f}"
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Only save event to DB once per second
                        if frame_count % frame_interval == 0:
                            current_video_time = start_time + timedelta(seconds=frame_count/fps)
                            events_to_save.append(
                                VehicleEvent(
                                    timestamp=current_video_time,
                                    video_source=filename,
                                    class_name=class_name,
                                    confidence=conf,
                                    event_type='detection'
                                )
                            )
            
            # Write annotated frame
            out.write(frame)

        cap.release()
        out.release()
        
        # Bulk Insert
        if events_to_save:
            print(f"Saving {len(events_to_save)} detection events to DB...")
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    session.add_all(events_to_save)
            print(f"Processing complete. Video saved to {output_path}")
        else:
            print(f"No vehicles detected in {filename}. Video saved anyway.")
            
    except Exception as e:
        print(f"Error processing video {filename}: {e}")
    finally:
        # Cleanup input temp file
        if os.path.exists(file_path):
            os.remove(file_path)
