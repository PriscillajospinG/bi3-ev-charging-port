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
