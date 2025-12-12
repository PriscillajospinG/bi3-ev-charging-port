from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.prediction import PredictionService

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.get("/demand")
def get_demand_forecast(days: int = 7, db: Session = Depends(get_db)):
    prediction = PredictionService(db)
    result = prediction.generate_forecast(days_history=60)
    return result

@router.get("/peaks")
def get_peak_predictions(db: Session = Depends(get_db)):
    prediction = PredictionService(db)
    result = prediction.generate_forecast()
    return {
        "peak_time": result.get("peak_demand_time", "N/A"),
        "peak_value": result.get("peak_demand_value", 0),
        "confidence": "85%"
    }

@router.get("/seasonal")
def get_seasonal_analysis():
    return {
        "growth_trend": "+5% Month over Month",
        "seasonal_factors": ["Weekend spike", "Holiday lull"]
    }
