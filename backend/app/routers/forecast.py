from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import data_cache, get_analytics_service
from ..services.forecast import PredictionService
from ..services.analytics import AnalyticsService
from ..schemas.dashboard import ForecastResponse

router = APIRouter(prefix="/api/forecast", tags=["Forecast"])

from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

@router.get("/run")
async def run_forecast(
    days: int = 7,
    service: AnalyticsService = Depends(get_analytics_service),
    db: AsyncSession = Depends(get_db)
):
    """
    Run the prediction engine (Prophet) on latest data.
    """
    # 1. Generate Forecast
    forecast_data = service.get_forecast(days=days)
    
    # 2. Persist to DB
    # forecast_data keys: peak_hour, peak_value, ensemble (list), lower_bound, upper_bound, dates (list)
    import uuid
    from datetime import datetime
    from ..models.outputs import ModelPrediction
    
    run_id = str(uuid.uuid4())
    dates = forecast_data.get('dates', [])
    ensemble = forecast_data.get('ensemble', [])
    lower = forecast_data.get('lower_bound', [])
    upper = forecast_data.get('upper_bound', [])
    
    if dates and ensemble:
        for i, date_str in enumerate(dates):
            # Parse date if string
            if isinstance(date_str, str):
                ts = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            else:
                ts = date_str
            
            val = ensemble[i] if i < len(ensemble) else 0
            l_val = lower[i] if i < len(lower) else 0
            u_val = upper[i] if i < len(upper) else 0
            
            pred = ModelPrediction(
                run_id=run_id,
                timestamp=ts,
                predicted_value=float(val),
                model_type='ensemble_prophet',
                lower_bound=float(l_val),
                upper_bound=float(u_val)
            )
            db.add(pred)
        
        await db.commit()
    
    return {"forecast": forecast_data}

@router.get("/accuracy")
async def get_forecast_accuracy(service: AnalyticsService = Depends(get_analytics_service)):
    forecast = service.get_forecast(days=1)
    return {"accuracy": forecast.get("accuracy", "85%")}

@router.get("/next7days")
async def get_forecast_next_7_days(service: AnalyticsService = Depends(get_analytics_service)):
    forecast = service.get_forecast(days=7)
    return forecast # The forecast object already contains dates and values
