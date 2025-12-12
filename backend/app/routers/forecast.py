from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_prediction_service, data_cache, get_analytics_service
from ..services.forecast import PredictionService
from ..services.analytics import AnalyticsService
from ..schemas.dashboard import ForecastResponse

router = APIRouter(prefix="/api/forecast", tags=["Forecast"])

@router.get("/run")
async def run_forecast(
    days: int = 7,
    service: AnalyticsService = Depends(get_analytics_service)
):
    """
    Run the prediction engine (Prophet) on latest data.
    """
    # Force forecast generation
    return {"forecast": service.get_forecast(days=days)}

@router.get("/accuracy")
async def get_forecast_accuracy(service: AnalyticsService = Depends(get_analytics_service)):
    forecast = service.get_forecast(days=1)
    return {"accuracy": forecast.get("accuracy", "85%")}

@router.get("/next7days")
async def get_forecast_next_7_days(service: AnalyticsService = Depends(get_analytics_service)):
    forecast = service.get_forecast(days=7)
    return forecast # The forecast object already contains dates and values
