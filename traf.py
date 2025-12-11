import cv2
from ultralytics import YOLO
from collections import defaultdict
import time

# Load the YOLO model
model = YOLO('yolo11l.pt')
class_list = model.names

# Open the video file
cap = cv2.VideoCapture('vehicle.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
frame_time = 1 / fps  # Time per frame in seconds

line_y_red = 430  # Red line position

# Dictionary to store object counts by class
class_counts = defaultdict(int)

# Dictionary to keep track of object IDs that have crossed the line
crossed_ids = set()

# Dictionary to store entry timestamp for each object ID
id_times = {}  # id_times[track_id] = {"class": class_name, "start": t_start}

frame_number = 0
video_start_time = time.time()  # Start real timestamp

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_number += 1
    # Use actual elapsed time since video started
    current_time = time.time() - video_start_time

    # Run YOLO tracking on the frame with better tracking parameters
    results = model.track(frame, persist=True, tracker="bytetrack.yaml", classes=[1, 2, 3, 5, 6, 7])

    if results[0].boxes.data is not None:
        boxes = results[0].boxes.xyxy.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        class_indices = results[0].boxes.cls.int().cpu().tolist()
        confidences = results[0].boxes.conf.cpu()

        cv2.line(frame, (690, line_y_red), (1130, line_y_red), (0, 0, 255), 3)

        for box, track_id, class_idx, conf in zip(boxes, track_ids, class_indices, confidences):
            x1, y1, x2, y2 = map(int, box)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            class_name = class_list[class_idx]

            # Initialize start time for new vehicle IDs
            if track_id not in id_times:
                id_times[track_id] = {"class": class_name, "start": current_time}

            # Calculate live duration
            duration = current_time - id_times[track_id]["start"]

            # Draw vehicle info
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            cv2.putText(frame, f"ID: {track_id} {class_name}", (x1, y1 - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Time: {duration:.2f}s", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Check if the object has crossed the red line
            if cy > line_y_red and track_id not in crossed_ids:
                crossed_ids.add(track_id)
                class_counts[class_name] += 1

        # Display counts on frame
        y_offset = 30
        for class_name, count in class_counts.items():
            cv2.putText(frame, f"{class_name}: {count}", (50, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_offset += 30

    frame_resized = cv2.resize(frame, (960, 540))
    cv2.imshow("YOLO Object Tracking & Counting with Live Timestamps", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Print all final durations after video ends
print("Vehicle durations in frame:")
for track_id, t_info in id_times.items():
    duration = current_time - t_info["start"]
    print(f"ID {track_id} ({t_info['class']}): {duration:.2f} seconds")

cap.release()
cv2.destroyAllWindows()
