# yolo_deepsort_timescale.py
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from collections import defaultdict
from datetime import datetime
from trafficdb import save_vehicle_event  # import your DB save function

# --------------------------
# Load YOLO model
# --------------------------
model = YOLO('yolo11l.pt')  # replace with your YOLOv11 weights
class_list = model.names

# --------------------------
# Open video
# --------------------------
cap = cv2.VideoCapture('Realistic_EV_Charging_Station_CCTV.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

# --------------------------
# Line position (for counting)
# --------------------------
line_y_red = 830  # y-coordinate of the red line

# --------------------------
# Tracker
# --------------------------
tracker = DeepSort(max_age=10)

# --------------------------
# Dictionaries for counting and timestamps
# --------------------------
class_counts = defaultdict(int)
vehicle_data = {}          # {track_id: {'entry_time': time, 'class': class_name, 'exit_time': time}}
active_tracks = set()      # Currently active track IDs

# --------------------------
# Processing loop
# --------------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True, classes=[1,2,3,5,6,7])  # car, truck, bus, motorbike, etc.

    if results[0].boxes.data is not None:
        boxes = results[0].boxes.xyxy.cpu()
        confidences = results[0].boxes.conf.cpu()
        class_indices = results[0].boxes.cls.int().cpu()

        detections = []
        for box, conf, class_idx in zip(boxes, confidences, class_indices):
            class_idx_int = int(class_idx)
            if class_idx_int in class_list:
                x1, y1, x2, y2 = map(int, box)
                class_name = class_list[class_idx_int]
                detections.append([[x1, y1, x2, y2], float(conf), class_name])

        tracks = tracker.update_tracks(detections, frame=frame)

        # Draw red line
        cv2.line(frame, (0, line_y_red), (frame.shape[1], line_y_red), (0,0,255), 3)

        current_frame_tracks = set()

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            x1, y1, x2, y2 = map(int, ltrb)
            cx = (x1 + x2)//2
            cy = (y1 + y2)//2
            class_name = track.det_class if hasattr(track, 'det_class') else "Unknown"

            current_frame_tracks.add(track_id)

            # Draw bounding box and ID
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.circle(frame, (cx, cy), 4, (0,0,255), -1)
            cv2.putText(frame, f"ID {track_id} ({class_name})", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

            # ENTRY TIME
            if cy > line_y_red and track_id not in vehicle_data:
                entry_time = datetime.now()
                vehicle_data[track_id] = {'entry_time': entry_time, 'class': class_name}
                class_counts[class_name] += 1
                print(f"ID {track_id} ({class_name}) entered at {entry_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Save to TimescaleDB
                save_vehicle_event(track_id, class_name, entry_time)

        # Check for vehicles that disappeared (EXIT TIME)
        disappeared_tracks = active_tracks - current_frame_tracks
        current_time = datetime.now()

        for disappeared_id in disappeared_tracks:
            if disappeared_id in vehicle_data and 'exit_time' not in vehicle_data[disappeared_id]:
                vehicle_data[disappeared_id]['exit_time'] = current_time
                vehicle_class = vehicle_data[disappeared_id]['class']
                print(f"ID {disappeared_id} ({vehicle_class}) exited at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Update exit time in DB
                save_vehicle_event(disappeared_id, vehicle_class, 
                                   vehicle_data[disappeared_id]['entry_time'],
                                   exit_time=current_time)

        active_tracks = current_frame_tracks

        # Display counts
        y_offset = 30
        for cls, count in class_counts.items():
            cv2.putText(frame, f"{cls}: {count}", (20, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            y_offset += 30

    frame_resized = cv2.resize(frame, (960,540))
    cv2.imshow("Vehicle Tracking & Counting", frame_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Handle vehicles still active at end of video
# Handle vehicles still active at end of video
final_time = datetime.now()
for active_id in active_tracks:
    if active_id in vehicle_data:
        # If exit_time doesn't exist, assign final_time
        if 'exit_time' not in vehicle_data[active_id]:
            vehicle_data[active_id]['exit_time'] = final_time
            vehicle_class = vehicle_data[active_id]['class']
            print(f"ID {active_id} ({vehicle_class}) exited at end of video ({final_time.strftime('%Y-%m-%d %H:%M:%S')})")
            
            # Save/update in TimescaleDB
            save_vehicle_event(
                active_id, 
                vehicle_class, 
                vehicle_data[active_id]['entry_time'], 
                exit_time=final_time
            )


cap.release()
cv2.destroyAllWindows()

# Print final entry/exit times
print("----- Vehicle Entry & Exit Times -----")
for track_id, data in vehicle_data.items():
    entry_str = data['entry_time'].strftime('%Y-%m-%d %H:%M:%S')
    exit_str = data.get('exit_time', "Still in frame")
    print(f"ID {track_id} ({data['class']}): Entry {entry_str}, Exit {exit_str}")
