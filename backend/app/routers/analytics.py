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

@router.get("/weekly")
async def get_analytics_weekly(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_weekly_stats()

@router.get("/heatmap")
async def get_analytics_heatmap(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_heatmap()

@router.get("/status")
async def get_analytics_status(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_status_distribution()
    
@router.get("/chargers")
async def get_analytics_chargers(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_charger_overview()
