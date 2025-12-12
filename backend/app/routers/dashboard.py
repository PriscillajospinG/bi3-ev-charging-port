from fastapi import APIRouter, Depends
from ..dependencies import get_analytics_service
from ..services.analytics import AnalyticsService
from ..schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(service: AnalyticsService = Depends(get_analytics_service)):
    """Get dashboard stats for the main dashboard page."""
    summary = service.get_summary_metrics()
    return summary


@router.get("/live", response_model=DashboardResponse)
async def get_dashboard_live(service: AnalyticsService = Depends(get_analytics_service)):
    # Aggregating all sub-components for the main dashboard view
    return DashboardResponse(
        revenue_panel=service.get_revenue_panel(),
        live_occupancy=service.get_live_occupancy(),
        traffic_analysis=service.get_traffic_analysis(),
        alerts=service.get_alerts(),
        charger_overview=service.get_charger_overview(),
        summary_metrics=service.get_summary_metrics(),
        utilization_trend=service.get_utilization_trend(),
        status_distribution=service.get_status_distribution()
    )

@router.get("/alerts")
async def get_dashboard_alerts(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_alerts()

@router.get("/performance")
async def get_dashboard_performance(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_charger_overview()

@router.get("/utilization-trend")
async def get_utilization_trend(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_utilization_trend()
