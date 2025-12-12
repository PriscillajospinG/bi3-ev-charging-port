# vehicle_metrics_timescale.py
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from datetime import datetime
from trafficdb import save_vehicle_metrics  # import your DB save function

# --------------------------
# Parameters
# --------------------------
VIDEO_PATH = "Realistic_EV_Charging_Station_CCTV.mp4"
LINE_Y_RED = 830
STATION_CAPACITY = 10
QUEUE_REGION = (50, 500, 900, 830)  # x1, y1, x2, y2

# --------------------------
# Load YOLO + Tracker
# --------------------------
model = YOLO("yolo11l.pt")
class_list = model.names
tracker = DeepSort(max_age=10)

# --------------------------
# Variables
# --------------------------
vehicle_data = {}          # track_id -> {'entry_time', 'class', 'exit_time'}
active_tracks = set()      # current active track IDs
session_count = 0          # total vehicles entered

# --------------------------
# Open video
# --------------------------
cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)

if not cap.isOpened():
    print(f"Error: Cannot open video file {VIDEO_PATH}")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO detection
    results = model.track(frame, persist=True, classes=[1,2,3,5,6,7])
    detections = []
    if results[0].boxes.data is not None:
        boxes = results[0].boxes.xyxy.cpu()
        confs = results[0].boxes.conf.cpu()
        class_indices = results[0].boxes.cls.int().cpu()

        for box, conf, cls_idx in zip(boxes, confs, class_indices):
            x1, y1, x2, y2 = map(int, box)
            class_name = class_list[int(cls_idx)]
            detections.append([[x1, y1, x2, y2], float(conf), class_name])

    tracks = tracker.update_tracks(detections, frame=frame)
    current_frame_tracks = set()

    # Draw entry line
    cv2.line(frame, (0, LINE_Y_RED), (frame.shape[1], LINE_Y_RED), (0,0,255), 3)

    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        cx, cy = (int(ltrb[0])+int(ltrb[2]))//2, (int(ltrb[1])+int(ltrb[3]))//2
        class_name = track.det_class if hasattr(track, 'det_class') else "Unknown"

        current_frame_tracks.add(track_id)

        # Entry detection
        if cy > LINE_Y_RED and track_id not in vehicle_data:
            vehicle_data[track_id] = {'entry_time': datetime.now(), 'class': class_name}
            session_count += 1

    # Check disappeared vehicles
    disappeared_tracks = active_tracks - current_frame_tracks
    current_time = datetime.now()
    for dt in disappeared_tracks:
        if dt in vehicle_data and 'exit_time' not in vehicle_data[dt]:
            vehicle_data[dt]['exit_time'] = current_time

    active_tracks = current_frame_tracks

    # Compute metrics
    vehicle_count = len(active_tracks)
    occupancy_rate = vehicle_count / STATION_CAPACITY * 100

    # Queue length
    x1_q, y1_q, x2_q, y2_q = QUEUE_REGION
    queue_length = 0
    for track in tracks:
        if track.is_confirmed():
            ltrb = track.to_ltrb()
            cx, cy = (int(ltrb[0])+int(ltrb[2]))//2, (int(ltrb[1])+int(ltrb[3]))//2
            if x1_q <= cx <= x2_q and y1_q <= cy <= y2_q:
                queue_length += 1

    # Timestamp
    timestamp = datetime.now()

    # Save metrics to TimescaleDB
    save_vehicle_metrics(timestamp, vehicle_count, session_count, occupancy_rate, queue_length)

    # Print metrics
    print(f"{timestamp} | Vehicles: {vehicle_count} | Session: {session_count} "
          f"| Occupancy: {occupancy_rate:.2f}% | Queue: {queue_length}")

    # Show frame
    frame_resized = cv2.resize(frame, (960,540))
    cv2.imshow("Vehicle Metrics", frame_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
