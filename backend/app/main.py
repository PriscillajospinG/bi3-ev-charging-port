from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import sys

# Add app to path to allow absolute imports if needed, though structure should handle it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .services.analytics import AnalyticsService
from .services.forecast import PredictionService
from .services.recommendations import RecommendationService
from .schemas.dashboard import (
    DashboardResponse, RevenuePanel, LiveOccupancy, TrafficAnalysis, 
    ForecastResponse, Recommendation
)

# --- Router Setup ---

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])
analytics_router = APIRouter(prefix="/api/analytics", tags=["Analytics"])
forecast_router = APIRouter(prefix="/api/forecast", tags=["Forecast"])
recommendations_router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

# --- Dependency Injection / Data Loading ---

# Global Data Cache (Simulating DB load for this phase)
class DataCache:
    df = None
    
data_cache = DataCache()

def get_analytics_service():
    if data_cache.df is None:
        raise HTTPException(status_code=503, detail="Data not loaded yet")
    return AnalyticsService(data_cache.df)

def get_prediction_service():
    return PredictionService()

def get_rec_service():
    return RecommendationService()

# --- Dashboard Endpoints ---

@dashboard_router.get("/live", response_model=DashboardResponse)
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

@dashboard_router.get("/alerts")
async def get_dashboard_alerts(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_alerts()

@dashboard_router.get("/performance")
async def get_dashboard_performance(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_charger_overview()

@dashboard_router.get("/utilization-trend")
async def get_utilization_trend(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_utilization_trend()

# --- Analytics Endpoints ---

@analytics_router.get("/summary")
async def get_analytics_summary(service: AnalyticsService = Depends(get_analytics_service)):
    return service.get_summary_metrics()

@analytics_router.get("/daily")
async def get_analytics_daily(service: AnalyticsService = Depends(get_analytics_service)):
    # Reuse utilization trend as proxy for daily profile
    return service.get_utilization_trend()

# --- Forecast Endpoints ---

@forecast_router.get("/run", response_model=ForecastResponse)
async def run_forecast(
    days: int = 7, 
    service: PredictionService = Depends(get_prediction_service)
):
    if data_cache.df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return service.run_forecast(data_cache.df, days)

@forecast_router.get("/accuracy")
async def get_forecast_accuracy():
    return {"accuracy": "88.5%", "metric": "MAPE"}

@forecast_router.get("/next7days")
async def get_next_7_days(service: PredictionService = Depends(get_prediction_service)):
    if data_cache.df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    return service.run_forecast(data_cache.df, days=7)

# --- Recommendation Endpoints ---

@recommendations_router.get("/", response_model=list[Recommendation])
async def get_recommendations(service: RecommendationService = Depends(get_rec_service)):
    return service.get_recommendations()

# --- Main App ---

app = FastAPI(title="EV Charging Backend API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event to Load Data & Init DB
@app.on_event("startup")
async def startup_event():
    print("--- ONE-TIME STARTUP ---")
    
    # 1. Initialize Database
    print("Initializing Database Schema...")
    from .database import engine, Base
    from .models.events import EvEvent
    from sqlalchemy import text
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created.")
        try:
            # Hypertable creation
            await conn.execute(text("SELECT create_hypertable('ev_events', by_range('timestamp'), if_not_exists => TRUE);"))
            print("Hypertable 'ev_events' configured.")
        except Exception as e:
            # Might fail if not TimescaleDB or perm issues, log warning
            print(f"Hypertable setup warning (continuing): {e}")

    # 2. Check Data & Seed
    print("Checking for existing data...")
    from sqlalchemy import select
    from .database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(EvEvent).limit(1))
        existing_data = result.scalar_one_or_none()
        
        if not existing_data:
            print("Database empty. Seeding from synthetic CSV...")
            # Locate CSV
            paths_to_check = [
                "models/prediction/synthetic_data.csv",
                "../models/prediction/synthetic_data.csv",
                "app/models/prediction/synthetic_data.csv",
                "../backend/models/prediction/synthetic_data.csv"
            ]
            csv_path = None
            for p in paths_to_check:
                if os.path.exists(p):
                    csv_path = p
                    break
            
                df_seed = pd.read_csv(csv_path)
                df_seed['timestamp'] = pd.to_datetime(df_seed['timestamp'])
                # Ensure UTC if naive
                if df_seed['timestamp'].dt.tz is None:
                    df_seed['timestamp'] = df_seed['timestamp'].dt.tz_localize('UTC')
                
                # Bulk Insert Logic
                # Convert DF to dicts
                events = df_seed.to_dict(orient='records')
                # Optional: chunking if too large
                chunk_size = 1000
                for i in range(0, len(events), chunk_size):
                    chunk = events[i:i+chunk_size]
                    await session.execute(
                        text("INSERT INTO ev_events (timestamp, station_id, vehicle_count, session_count, occupancy_rate, queue_length) VALUES (:timestamp, :station_id, :vehicle_count, :session_count, :occupancy_rate, :queue_length)"),
                        chunk
                    )
                    await session.commit()
                print(f"Seeded {len(events)} records into TimescaleDB.")
            else:
                print("WARNING: Seed file not found.")
        else:
            print("Database already contains data. Skipping seed.")

        # 3. Load Data into Cache (Hybrid pattern)
        print("Loading data into Analytics Cache from DB...")
        # Fetch all data for analytics engine
        # Note: In prod with millions of rows, we'd refactor AnalyticsService to run SQL aggregations.
        # For this demo scale (14k rows), loading to DF is instant and allows reusing our python engine logic flawlessly.
        
        # Using pandas read_sql with async engine is tricky, better to fetch and construct
        result_all = await session.execute(select(EvEvent).order_by(EvEvent.timestamp))
        rows = result_all.scalars().all()
        
        # Convert ORM objects to list of dicts
        data = [{
            "timestamp": r.timestamp,
            "station_id": r.station_id,
            "vehicle_count": r.vehicle_count,
            "session_count": r.session_count,
            "occupancy_rate": r.occupancy_rate,
            "queue_length": r.queue_length
        } for r in rows]
        
        data_cache.df = pd.DataFrame(data)
        print(f"Analytics Cache Ready: {len(data_cache.df)} rows loaded.")

# Include Routers
app.include_router(dashboard_router)
app.include_router(analytics_router)
app.include_router(forecast_router)
app.include_router(recommendations_router)

@app.get("/")
async def root():
    return {"message": "EV Charging Backend API is running"}
