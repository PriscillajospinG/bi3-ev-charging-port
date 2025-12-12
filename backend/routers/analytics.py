from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/utilization")
def get_utilization_data(window: str = "24h", db: Session = Depends(get_db)):
    analytics = AnalyticsService(db)
    return analytics.get_daily_utilization_trend(window)

@router.get("/traffic")
def get_traffic_data(window: str = "24h", db: Session = Depends(get_db)):
    # Reusing trend logic for traffic (vehicle count)
    analytics = AnalyticsService(db)
    df = analytics.get_data(window)
    if df.empty: return []
    
    # Resample
    resample_rule = '1H' if window == '24h' else '1D'
    hourly = df.set_index('timestamp').resample(resample_rule)['vehicle_count'].sum().reset_index()
    
    data = []
    for _, row in hourly.tail(30).iterrows():
        ts = row['timestamp']
        label = ts.strftime("%H:%M") if window == '24h' else ts.strftime("%a")
        data.append({
            "time": label,
            "value": int(row['vehicle_count'])
        })
    return data

@router.get("/heatmap")
def get_heatmap_data(db: Session = Depends(get_db)):
    # Mocking heatmap structure as complex aggregation is needed
    return {
        "Mon": [10, 20, 40, 60, 50, 30, 20, 10],
        "Tue": [15, 25, 45, 65, 55, 35, 25, 15],
        "Wed": [10, 20, 40, 60, 50, 30, 20, 10],
        "Thu": [12, 22, 42, 62, 52, 32, 22, 12],
        "Fri": [20, 30, 50, 70, 60, 40, 30, 20],
        "Sat": [30, 40, 60, 80, 70, 50, 40, 30],
        "Sun": [25, 35, 55, 75, 65, 45, 35, 25]
    }

@router.get("/occupancy")
def get_occupancy_stats(db: Session = Depends(get_db)):
    analytics = AnalyticsService(db)
    return analytics.compute_metrics("24h") # Reuse summary
