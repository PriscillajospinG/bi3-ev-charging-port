import cv2
from ultralytics import YOLO
from collections import defaultdict
import time
from deep_sort_realtime.deepsort_tracker import DeepSort  # MVSort can be implemented via DeepSort

# Load the YOLO model
model = YOLO('yolo11l.pt')
class_list = model.names

# Open the video file
cap = cv2.VideoCapture('vehicle.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

line_y_red = 430  # Red line position

# Initialize DeepSort tracker (acts as MVSORT)
tracker = DeepSort(max_age=30)

# Dictionaries to store timestamps
entry_time = {}   # {track_id: entry_time}
exit_time = {}    # {track_id: exit_time}
crossed_ids = set()
class_counts = defaultdict(int)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO inference
    results = model.predict(frame, classes=[1,2,3,5,6,7])

    detections = []
    if results[0].boxes.data is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        class_indices = results[0].boxes.cls.int().cpu().tolist()
        confidences = results[0].boxes.conf.cpu().numpy()

        # Prepare detections for MVSORT (x1, y1, x2, y2, conf, class_id)
        for box, conf, cls in zip(boxes, confidences, class_indices):
            x1, y1, x2, y2 = box
            detections.append([x1, y1, x2, y2, conf, cls])

    # Update tracker
    tracks = tracker.update_tracks(detections, frame=frame)

    cv2.line(frame, (690, line_y_red), (1130, line_y_red), (0, 0, 255), 3)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()  # left, top, right, bottom
        x1, y1, x2, y2 = map(int, ltrb)
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        class_idx = track.det_class
        class_name = class_list[class_idx]

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        cv2.putText(frame, f"ID:{track_id} {class_name}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

        # Record entry timestamp
        if cy > line_y_red and track_id not in crossed_ids:
            crossed_ids.add(track_id)
            class_counts[class_name] += 1
            entry_time[track_id] = time.time()  # Record entry time

    # Check for exited vehicles (MVSORT deletes old tracks)
    active_ids = {t.track_id for t in tracks if t.is_confirmed()}
    for t_id in list(entry_time.keys()):
        if t_id not in active_ids and t_id not in exit_time:
            exit_time[t_id] = time.time()  # Record exit time

    # Display counts and timestamps
    y_offset = 30
    for class_name, count in class_counts.items():
        cv2.putText(frame, f"{class_name}: {count}", (50, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        y_offset += 30

    # Show frame
    frame_resized = cv2.resize(frame, (960, 540))
    cv2.imshow("YOLO + MVSORT Tracking", frame_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Print timestamps
print("Entry times:", entry_time)
print("Exit times:", exit_time)
