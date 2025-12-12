from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import sys

# Add app to path to allow absolute imports if needed, though structure should handle it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .dependencies import data_cache
from .routers import dashboard, analytics, forecast, recommendations, frontend

# --- Main App ---

app = FastAPI(title="EV Charging Backend API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(dashboard.router)
app.include_router(analytics.router)
app.include_router(forecast.router)
app.include_router(recommendations.router)
app.include_router(frontend.router)

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
                print(f"Checking path: {os.path.abspath(p)}")
                if os.path.exists(p):
                    print(f"Found at: {p}")
                    csv_path = p
                    break
            print(f"CWD: {os.getcwd()}")
            
            if csv_path:
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
        
        # 4. Generate Consistent Session Data for Detail Views
        # Use DataSimulator to create a consistent view of chargers/sessions
        from .models.dashboard.dashboard_engine import DataSimulator
        
        print("Generating consistent session/charger data...")
        simulator = DataSimulator(data_cache.df)
        data_cache.session_df = simulator.get_charger_level_data()
        print(f"Session Cache Ready: {len(data_cache.session_df)} sessions generated.")

# --- WebSocket ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Basic Echo/Ack for now to keep frontend happy
            if data.get("type") == "subscribe":
                stream = data.get("payload", {}).get("stream")
                await websocket.send_json({
                    "type": "connected",
                    "payload": {"status": f"Subscribed to {stream}"}
                })
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket Error: {e}")

@app.get("/")
async def root():
    return {"message": "EV Charging Backend API is running"}
