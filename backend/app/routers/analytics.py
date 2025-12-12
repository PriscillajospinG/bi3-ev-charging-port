from fastapi import APIRouter, Depends
from ..dependencies import get_analytics_service
from ..services.analytics import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/summary")
async def get_analytics_summary(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_summary_metrics()

@router.get("/daily")
async def get_analytics_daily(service: AnalyticsService = Depends(get_analytics_service)):
    # Reuse utilization trend as proxy for daily profile
    return service.get_utilization_trend()
