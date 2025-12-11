import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import defaultdict
import time

# --------------------------
# Load YOLO model
# --------------------------
model = YOLO('yolo11l.pt')  # replace with your YOLOv11 weights
class_list = model.names

# --------------------------
# Open video
# --------------------------
cap = cv2.VideoCapture('vehicle.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

# --------------------------
# Line position (for counting)
# --------------------------
line_y_red = 430  # y-coordinate of the red line

# --------------------------
# Tracker
# --------------------------
tracker = DeepSort(max_age=10)  # You can adjust max_age for lost track

# --------------------------
# Dictionaries for counting and timestamps
# --------------------------
class_counts = defaultdict(int)
vehicle_entry_times = {}   # {track_id: entry_time}
vehicle_exit_times = {}    # {track_id: exit_time}
active_tracks = set()      # Currently active track IDs

# --------------------------
# Processing loop
# --------------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO detection for specific vehicle classes
    results = model.track(frame, persist=True, classes=[1,2,3,5,6,7])  # car, truck, bus, motorbike, etc.

    if results[0].boxes.data is not None:
        boxes = results[0].boxes.xyxy.cpu()  # x1,y1,x2,y2
        confidences = results[0].boxes.conf.cpu()  # confidence
        class_indices = results[0].boxes.cls.int().cpu()  # class index

        # Prepare detections for DeepSort
        detections = []
        for box, conf, class_idx in zip(boxes, confidences, class_indices):
            class_idx_int = int(class_idx)
            if class_idx_int in class_list:
                x1, y1, x2, y2 = map(int, box)
                class_name = class_list[class_idx_int]
                detections.append([[x1, y1, x2, y2], float(conf), class_name])
            else:
                print(f"Warning: Unknown class index {class_idx_int}")

        # Update tracker
        tracks = tracker.update_tracks(detections, frame=frame)

        # Draw red line
        cv2.line(frame, (0, line_y_red), (frame.shape[1], line_y_red), (0,0,255), 3)

        # Process each track
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            x1, y1, x2, y2 = map(int, ltrb)
            cx = (x1 + x2)//2
            cy = (y1 + y2)//2
            class_name = track.det_class if hasattr(track, 'det_class') else "Unknown"

            # Draw bounding box, ID, and class
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.circle(frame, (cx, cy), 4, (0,0,255), -1)
            cv2.putText(frame, f"ID {track_id} ({class_name})", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

            # ENTRY TIME (first time crosses the line)
            if cy > line_y_red and track_id not in vehicle_entry_times:
                vehicle_entry_times[track_id] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # seconds
                class_counts[class_name] += 1
                print(f"ID {track_id} ({class_name}) entered at {vehicle_entry_times[track_id]:.2f} s")

            # Note: Exit time tracking removed due to DeepSort implementation complexity
            # Vehicles are counted when they first cross the line

        # Update active tracks and check for disappeared vehicles
        current_frame_tracks = {track.track_id for track in tracks if track.is_confirmed()}

        # Check for vehicles that disappeared (exit time)
        disappeared_tracks = active_tracks - current_frame_tracks
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        for disappeared_id in disappeared_tracks:
            if disappeared_id in vehicle_entry_times and disappeared_id not in vehicle_exit_times:
                vehicle_exit_times[disappeared_id] = current_time
                print(f"ID {disappeared_id} exited at {vehicle_exit_times[disappeared_id]:.2f} s")

        # Update active tracks for next frame
        active_tracks = current_frame_tracks

        # Display counts
        y_offset = 30
        for cls, count in class_counts.items():
            cv2.putText(frame, f"{cls}: {count}", (20, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            y_offset += 30

    # Resize and show frame
    frame_resized = cv2.resize(frame, (960,540))
    cv2.imshow("Vehicle Tracking & Counting", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Handle vehicles still active at end of video
final_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
for active_id in active_tracks:
    if active_id in vehicle_entry_times and active_id not in vehicle_exit_times:
        vehicle_exit_times[active_id] = final_time
        print(f"ID {active_id} exited at end of video ({vehicle_exit_times[active_id]:.2f} s)")

# Release
cap.release()
cv2.destroyAllWindows()

# Print final entry/exit times
print("----- Vehicle Entry & Exit Times -----")
for vid in vehicle_entry_times:
    entry = vehicle_entry_times[vid]
    exit_time = vehicle_exit_times.get(vid, "Still in frame")
    print(f"ID {vid}: Entry {entry:.2f}s, Exit {exit_time}")
