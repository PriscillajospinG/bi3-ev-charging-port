from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, index=True)  # To group predictions from a single execution
    timestamp = Column(DateTime(timezone=True), index=True) # The future time being predicted
    predicted_value = Column(Float)
    model_type = Column(String) # 'ensemble', 'prophet', etc.
    lower_bound = Column(Float, nullable=True)
    upper_bound = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    priority = Column(String)
    location = Column(String)
    expected_impact = Column(String)
    estimated_cost = Column(String)
    roi_timeline = Column(String)
    category = Column(String)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="Proposed") # Proposed, Implemented, Rejected
