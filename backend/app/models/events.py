from sqlalchemy import Column, Integer, Float, String, DateTime
from ..database import Base

class EvEvent(Base):
    __tablename__ = "ev_events"

    # TimescaleDB hypertable logic in SQL usually handles the partitioning by timestamp.
    # We define the schema here.
    # Composite PK might be needed if timestamp is not unique globally, 
    # but (timestamp, station_id) is usually unique.
    
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    station_id = Column(String, primary_key=True)
    vehicle_count = Column(Integer)
    session_count = Column(Integer)
    occupancy_rate = Column(Float)
    queue_length = Column(Integer)

class VehicleEvent(Base):
    __tablename__ = "vehicle_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    video_source = Column(String) # Filename or Camera ID
    class_name = Column(String)   # car, truck, bus
    confidence = Column(Float)
    event_type = Column(String)   # 'entry', 'exit', 'detection'
