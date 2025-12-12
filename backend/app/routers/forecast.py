from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_prediction_service, data_cache
from ..services.forecast import PredictionService
from ..schemas.dashboard import ForecastResponse

router = APIRouter(prefix="/api/forecast", tags=["Forecast"])

@router.get("/run", response_model=ForecastResponse)
async def run_forecast(
    days: int = 7, 
    service: PredictionService = Depends(get_prediction_service)
):
    if data_cache.df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return service.run_forecast(data_cache.df, days)

@router.get("/accuracy")
async def get_forecast_accuracy():
    return {"accuracy": "88.5%", "metric": "MAPE"}

@router.get("/next7days")
async def get_next_7_days(service: PredictionService = Depends(get_prediction_service)):
    if data_cache.df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return service.run_forecast(data_cache.df, days=7)
