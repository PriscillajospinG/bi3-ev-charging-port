from fastapi import APIRouter, Depends
from typing import List
from ..dependencies import get_analytics_service
from ..services.analytics import AnalyticsService
from ..schemas.dashboard import (
    FrontendMetrics, FrontendCharger, FrontendUtilizationItem, 
    FrontendOccupancyItem, Alert
)

router = APIRouter(tags=["Frontend Integration"])

@router.get("/api/metrics/current", response_model=FrontendMetrics, tags=["Metrics"])
async def get_current_metrics(service: AnalyticsService = Depends(get_analytics_service)):
    return service.frontend_get_current_metrics()

@router.get("/api/chargers", response_model=List[FrontendCharger], tags=["Chargers"])
async def get_chargers(service: AnalyticsService = Depends(get_analytics_service)):
    return service.frontend_get_chargers()

@router.get("/api/analytics/utilization", response_model=List[FrontendUtilizationItem], tags=["Analytics"])
async def get_frontend_utilization(range: str = "24h", service: AnalyticsService = Depends(get_analytics_service)):
    return service.frontend_get_utilization(range)

@router.get("/api/analytics/occupancy", response_model=List[FrontendOccupancyItem], tags=["Analytics"])
async def get_frontend_occupancy(service: AnalyticsService = Depends(get_analytics_service)):
    return service.frontend_get_occupancy()

@router.get("/api/alerts", response_model=List[Alert], tags=["Alerts"])
async def get_frontend_alerts(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_alerts()
