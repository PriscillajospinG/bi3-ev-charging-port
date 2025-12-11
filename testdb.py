from trafficdb import save_vehicle_event
from datetime import datetime

save_vehicle_event(999, "car", datetime.now(), datetime.now())
print("Test insert successful!")
