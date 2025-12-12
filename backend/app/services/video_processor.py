import cv2
import os
import asyncio
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import AsyncSessionLocal
from ..models.events import VehicleEvent

# Global model instance to avoid reloading
_model = None

# In-memory status tracker for video processing jobs
# Format: {filename: {status, started_at, completed_at, total_frames, processed_frames, detections_count, error}}
processing_status: Dict[str, Dict[str, Any]] = {}

def get_processing_status(filename: str) -> Dict[str, Any]:
    """Get the processing status for a video file."""
    return processing_status.get(filename, {"status": "not_found"})

def get_all_processing_status() -> Dict[str, Dict[str, Any]]:
    """Get all processing statuses."""
    return processing_status

def update_status(filename: str, **kwargs):
    """Update the processing status for a video file."""
    if filename not in processing_status:
        processing_status[filename] = {
            "status": "pending",
            "started_at": None,
            "completed_at": None,
            "total_frames": 0,
            "processed_frames": 0,
            "detections_count": 0,
            "error": None,
            "detection_summary": {}
        }
    processing_status[filename].update(kwargs)

def get_yolo_model():
    """Lazy load the YOLO model only when needed."""
    global _model
    if _model is None:
        print("Loading YOLOv11 model...")
        # Lazy import to avoid loading torch at module import time
        from ultralytics import YOLO
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
    
    # Initialize status tracking
    update_status(filename, 
                  status="processing", 
                  started_at=datetime.now().isoformat(),
                  error=None)
    
    detection_summary = {}  # Track counts by class
    
    try:
        model = get_yolo_model()
        print("Model retrieved.")
        
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print(f"ERROR: Could not open video file: {file_path}")
            update_status(filename, status="failed", error="Could not open video file")
            return

        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Video opened. FPS: {fps}, Total Frames: {total_frames}")
        
        update_status(filename, total_frames=total_frames)
        
        frame_interval = int(fps) # Process 1 frame per second to save resources
        
        events_to_save = []
        frame_count = 0
        processed_count = 0
        
        # We start "timestamp" at now, and increment by video time
        start_time = datetime.now()
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            if frame_count % frame_interval != 0:
                continue
            
            processed_count += 1
            
            # Update progress every 10 processed frames
            if processed_count % 10 == 0:
                update_status(filename, processed_frames=processed_count)
                
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
                        # Update detection summary
                        detection_summary[class_name] = detection_summary.get(class_name, 0) + 1
            
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
        
        # Update final status
        update_status(filename, 
                      status="completed",
                      completed_at=datetime.now().isoformat(),
                      processed_frames=processed_count,
                      detections_count=len(events_to_save),
                      detection_summary=detection_summary)
            
    except Exception as e:
        print(f"Error processing video {filename}: {e}")
        update_status(filename, 
                      status="failed", 
                      error=str(e),
                      completed_at=datetime.now().isoformat())
    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)
