import cv2
import os
import asyncio
import math
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from collections import OrderedDict

from ..database import AsyncSessionLocal
from ..models.events import VehicleEvent

# Global model instance to avoid reloading
_model = None

# In-memory status tracker for video processing jobs
# Format: {filename: {status, started_at, completed_at, total_frames, processed_frames, detections_count, error}}
processing_status: Dict[str, Dict[str, Any]] = {}


class CentroidTracker:
    """
    Simple centroid-based object tracker that assigns unique IDs to objects
    and tracks them across frames based on their center position.
    Also tracks dwell time and queue length metrics.
    """
    def __init__(self, max_disappeared: int = 30, max_distance: float = 100.0):
        """
        Args:
            max_disappeared: Number of frames an object can be missing before being deregistered
            max_distance: Maximum distance (pixels) to consider two centroids as the same object
        """
        self.next_object_id = 0
        self.objects: OrderedDict[int, Tuple[float, float, str]] = OrderedDict()  # id -> (cx, cy, class_name)
        self.disappeared: Dict[int, int] = {}  # id -> frames disappeared
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.counted_ids: set = set()  # Track which IDs have been counted
        
        # Dwell time tracking
        self.entry_times: Dict[int, float] = {}  # id -> entry timestamp (seconds from video start)
        self.exit_times: Dict[int, float] = {}   # id -> exit timestamp (seconds from video start)
        self.dwell_times: Dict[int, float] = {}  # id -> dwell time in seconds
        self.class_names: Dict[int, str] = {}    # id -> class name (for completed tracks)
        
        # Queue length tracking
        self.queue_history: List[Tuple[float, int]] = []  # (timestamp, queue_length)
        self.max_queue_length = 0
        self.current_time = 0.0  # Current video time in seconds
    
    def set_current_time(self, time_seconds: float):
        """Set the current video time for dwell calculations."""
        self.current_time = time_seconds
    
    def register(self, centroid: Tuple[float, float], class_name: str) -> int:
        """Register a new object with the next available ID."""
        object_id = self.next_object_id
        self.objects[object_id] = (centroid[0], centroid[1], class_name)
        self.disappeared[object_id] = 0
        self.next_object_id += 1
        
        # Record entry time
        self.entry_times[object_id] = self.current_time
        self.class_names[object_id] = class_name
        
        return object_id
    
    def deregister(self, object_id: int):
        """Deregister an object ID and calculate its dwell time."""
        if object_id in self.objects:
            # Record exit time and calculate dwell time
            self.exit_times[object_id] = self.current_time
            if object_id in self.entry_times:
                dwell = self.current_time - self.entry_times[object_id]
                self.dwell_times[object_id] = dwell
            
            del self.objects[object_id]
        if object_id in self.disappeared:
            del self.disappeared[object_id]
    
    def update(self, detections: List[Tuple[Tuple[float, float], str, float]]) -> List[Tuple[int, str, bool]]:
        """
        Update the tracker with new detections.
        
        Args:
            detections: List of ((cx, cy), class_name, confidence) tuples
            
        Returns:
            List of (object_id, class_name, is_new) tuples for each detection
        """
        results = []
        
        # If no detections, mark all existing objects as disappeared
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            # Record queue length
            self._record_queue_length()
            return results
        
        # If no existing objects, register all detections as new
        if len(self.objects) == 0:
            for (centroid, class_name, conf) in detections:
                object_id = self.register(centroid, class_name)
                is_new = object_id not in self.counted_ids
                if is_new:
                    self.counted_ids.add(object_id)
                results.append((object_id, class_name, is_new))
            # Record queue length
            self._record_queue_length()
            return results
        
        # Match existing objects to new detections based on distance
        object_ids = list(self.objects.keys())
        object_centroids = [(self.objects[oid][0], self.objects[oid][1]) for oid in object_ids]
        
        input_centroids = [(d[0], d[1], d[2]) for d in detections]  # (centroid, class_name, conf)
        
        # Compute distance matrix
        distances = []
        for (cx, cy) in object_centroids:
            row = []
            for (centroid, class_name, conf) in input_centroids:
                dist = math.sqrt((cx - centroid[0])**2 + (cy - centroid[1])**2)
                row.append(dist)
            distances.append(row)
        
        # Match objects using greedy assignment (closest first)
        used_rows = set()
        used_cols = set()
        matches = []
        
        # Create list of all (distance, row, col) and sort by distance
        all_pairs = []
        for row_idx, row in enumerate(distances):
            for col_idx, dist in enumerate(row):
                all_pairs.append((dist, row_idx, col_idx))
        all_pairs.sort(key=lambda x: x[0])
        
        for dist, row_idx, col_idx in all_pairs:
            if row_idx in used_rows or col_idx in used_cols:
                continue
            if dist > self.max_distance:
                continue
            matches.append((row_idx, col_idx, dist))
            used_rows.add(row_idx)
            used_cols.add(col_idx)
        
        # Update matched objects
        for row_idx, col_idx, dist in matches:
            object_id = object_ids[row_idx]
            centroid, class_name, conf = input_centroids[col_idx]
            self.objects[object_id] = (centroid[0], centroid[1], class_name)
            self.disappeared[object_id] = 0
            is_new = object_id not in self.counted_ids
            if is_new:
                self.counted_ids.add(object_id)
            results.append((object_id, class_name, is_new))
        
        # Register unmatched detections as new objects
        unmatched_cols = set(range(len(input_centroids))) - used_cols
        for col_idx in unmatched_cols:
            centroid, class_name, conf = input_centroids[col_idx]
            object_id = self.register(centroid, class_name)
            is_new = object_id not in self.counted_ids
            if is_new:
                self.counted_ids.add(object_id)
            results.append((object_id, class_name, is_new))
        
        # Mark unmatched existing objects as disappeared
        unmatched_rows = set(range(len(object_ids))) - used_rows
        for row_idx in unmatched_rows:
            object_id = object_ids[row_idx]
            self.disappeared[object_id] += 1
            if self.disappeared[object_id] > self.max_disappeared:
                self.deregister(object_id)
        
        # Record queue length
        self._record_queue_length()
        
        return results
    
    def _record_queue_length(self):
        """Record the current queue length at this timestamp."""
        current_queue = len(self.objects)
        self.queue_history.append((self.current_time, current_queue))
        if current_queue > self.max_queue_length:
            self.max_queue_length = current_queue
    
    def get_current_queue_length(self) -> int:
        """Get the current number of vehicles being tracked (queue length)."""
        return len(self.objects)
    
    def get_max_queue_length(self) -> int:
        """Get the maximum queue length observed during tracking."""
        return self.max_queue_length
    
    def get_average_queue_length(self) -> float:
        """Get the average queue length over time."""
        if not self.queue_history:
            return 0.0
        total = sum(q for _, q in self.queue_history)
        return total / len(self.queue_history)
    
    def get_average_dwell_time(self) -> float:
        """Get the average dwell time of all completed vehicle tracks in seconds."""
        if not self.dwell_times:
            # If no vehicles have exited, calculate dwell time for active ones
            if self.entry_times:
                active_dwells = [self.current_time - entry for entry in self.entry_times.values()]
                if active_dwells:
                    return sum(active_dwells) / len(active_dwells)
            return 0.0
        return sum(self.dwell_times.values()) / len(self.dwell_times)
    
    def get_dwell_time_by_class(self) -> Dict[str, float]:
        """Get average dwell time by vehicle class."""
        class_dwells: Dict[str, List[float]] = {}
        for obj_id, dwell in self.dwell_times.items():
            class_name = self.class_names.get(obj_id, 'unknown')
            if class_name not in class_dwells:
                class_dwells[class_name] = []
            class_dwells[class_name].append(dwell)
        
        return {cls: (sum(dwells) / len(dwells)) for cls, dwells in class_dwells.items() if dwells}
    
    def get_unique_counts(self) -> Dict[str, int]:
        """Get the count of unique vehicles by class."""
        counts = {}
        for object_id in self.counted_ids:
            class_name = self.class_names.get(object_id)
            if class_name:
                counts[class_name] = counts.get(class_name, 0) + 1
        return counts
    
    def get_total_unique_count(self) -> int:
        """Get the total number of unique vehicles detected."""
        return len(self.counted_ids)

def get_processing_status(filename: str) -> Dict[str, Any]:
    """Get the processing status for a video file."""
    return processing_status.get(filename, {"status": "not_found"})

def get_all_processing_status() -> Dict[str, Dict[str, Any]]:
    """Get all processing statuses."""
    return processing_status

def reset_processing_status():
    """Reset all processing statuses."""
    global processing_status
    processing_status = {}
    return True

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
    Uses centroid tracking to count each vehicle only once.
    """
    print(f"Starting processing for {filename}...")
    print(f"File path: {os.path.abspath(file_path)}")
    
    # Initialize status tracking
    update_status(filename, 
                  status="processing", 
                  started_at=datetime.now().isoformat(),
                  error=None)
    
    # Initialize the centroid tracker for this video
    # max_disappeared=5 means a vehicle can be missing for 5 frames before considered gone
    # max_distance=150 means objects within 150 pixels are considered the same
    tracker = CentroidTracker(max_disappeared=5, max_distance=150)
    unique_vehicle_counts = {}  # Track unique counts by class
    
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
        
        frame_interval = max(1, int(fps / 3))  # Process ~3 frames per second for better tracking
        
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
            
            # Calculate current video time in seconds and update tracker
            video_time_seconds = frame_count / fps
            tracker.set_current_time(video_time_seconds)
            
            # Update progress every 10 processed frames
            if processed_count % 10 == 0:
                update_status(filename, 
                              processed_frames=frame_count,
                              queue_length=tracker.get_current_queue_length(),
                              avg_dwell_time=round(tracker.get_average_dwell_time(), 2))
                
            # Run Inference
            results = model(frame, verbose=False)
            
            # Extract detections with centroids
            detections = []  # List of ((cx, cy), class_name, confidence)
            if results and results[0].boxes:
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]
                    conf = float(box.conf[0])
                    
                    # Filter for vehicles
                    if class_name in ['car', 'truck', 'bus', 'motorcycle'] and conf > 0.5:
                        # Get bounding box and calculate centroid
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        cx = (x1 + x2) / 2
                        cy = (y1 + y2) / 2
                        detections.append(((cx, cy), class_name, conf))
            
            # Update tracker and get tracked objects
            tracked_objects = tracker.update(detections)
            
            # Create events only for NEW vehicles (first time seen)
            current_video_time = start_time + timedelta(seconds=frame_count/fps)
            
            for object_id, obj_class, is_new in tracked_objects:
                if is_new:
                    # This is a new unique vehicle - count it!
                    unique_vehicle_counts[obj_class] = unique_vehicle_counts.get(obj_class, 0) + 1
                    
                    # Save detection event for new vehicles only
                    events_to_save.append(
                        VehicleEvent(
                            timestamp=current_video_time,
                            video_source=filename,
                            class_name=obj_class,
                            confidence=0.9,  # Average confidence for tracked object
                            event_type='unique_detection'
                        )
                    )

        cap.release()
        
        # Bulk Insert
        if events_to_save:
            print(f"Saving {len(events_to_save)} unique vehicle detections to DB...")
            print(f"Unique vehicle counts: {unique_vehicle_counts}")
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    session.add_all(events_to_save)
            print(f"Processing complete for {filename}.")
        else:
            print(f"No vehicles detected in {filename}.")
        
        # Calculate final metrics
        total_unique = tracker.get_total_unique_count()
        max_queue = tracker.get_max_queue_length()
        avg_queue = round(tracker.get_average_queue_length(), 2)
        avg_dwell = round(tracker.get_average_dwell_time(), 2)
        dwell_by_class = {k: round(v, 2) for k, v in tracker.get_dwell_time_by_class().items()}
        
        print(f"📊 Video Analysis Complete for {filename}:")
        print(f"   - Unique Vehicles: {total_unique}")
        print(f"   - Max Queue Length: {max_queue}")
        print(f"   - Average Queue Length: {avg_queue}")
        print(f"   - Average Dwell Time: {avg_dwell}s")
        print(f"   - Dwell Time by Class: {dwell_by_class}")
        
        # Update final status with all metrics
        update_status(filename, 
                      status="completed",
                      completed_at=datetime.now().isoformat(),
                      processed_frames=total_frames,
                      detections_count=total_unique,
                      detection_summary=unique_vehicle_counts,
                      max_queue_length=max_queue,
                      avg_queue_length=avg_queue,
                      avg_dwell_time=avg_dwell,
                      dwell_time_by_class=dwell_by_class)
            
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
