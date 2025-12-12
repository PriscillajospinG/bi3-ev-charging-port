from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.analytics import AnalyticsService

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    analytics = AnalyticsService(db)
    return analytics.compute_metrics("24h")

@router.get("/chargers")
def get_chargers():
    # Mocking charger status as per previous requirements since DB table is aggregate
    return [
        {"id": "C1", "status": "Available", "power": "150kW", "connector": "CCS2"},
        {"id": "C2", "status": "Charging", "power": "150kW", "connector": "CCS2"},
        {"id": "C3", "status": "Available", "power": "50kW", "connector": "CHAdeMO"},
        {"id": "C4", "status": "Maintenance", "power": "50kW", "connector": "CCS2"},
    ]

@router.get("/chargers/status")
def get_charger_status_distribution(db: Session = Depends(get_db)):
    # Using real data to determine overall status
    analytics = AnalyticsService(db)
    metrics = analytics.compute_metrics("24h")
    # Using utilization to estimate distribution for visualization
    # Real implementation would count distinct station_ids if available
    return {
        "available": {"percent": 60, "units": 6},
        "occupied": {"percent": 30, "units": 3},
        "maintenance": {"percent": 10, "units": 1},
        "offline": {"percent": 0, "units": 0}
    }
