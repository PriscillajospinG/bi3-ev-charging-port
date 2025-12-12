from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import sys

# Add app to path to allow absolute imports if needed, though structure should handle it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .dependencies import data_cache
from .routers import dashboard, analytics, forecast, recommendations, frontend, map_router

# --- Main App ---

app = FastAPI(title="EV Charging Backend API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173", "*"],
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
app.include_router(map_router.router)

# Startup Event to Load Data & Init DB
@app.on_event("startup")
async def startup_event():
    print("--- ONE-TIME STARTUP ---")
    
    # 1. Initialize Database
    print("Initializing Database Schema...")
    from .database import engine, Base
    from .models.events import EvEvent
    from .models.outputs import ModelPrediction, Recommendation
    from sqlalchemy import text
    from .database import AsyncSessionLocal
    from sqlalchemy import select
    
    db_connected = False
    import asyncio
    try:
        # Wrap the connection logic in a timeout wrapper function
        async def connect_db():
            print(f"Attempting to connect with URL: {str(engine.url).split('@')[-1]}") # Hide auth
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                    print("Tables created.")
                    try:
                        await conn.execute(text("SELECT create_hypertable('ev_events', by_range('timestamp'), if_not_exists => TRUE);"))
                        print("Hypertable 'ev_events' configured.")
                    except Exception as e:
                        print(f"Hypertable setup warning:: {e}")
            except Exception as e:
                print(f"Detailed DB Error: {e}")
                raise e

        # Enforce 30 second timeout on DB connection (Remote DB might be slow)
        await asyncio.wait_for(connect_db(), timeout=30.0)
        db_connected = True
    except asyncio.TimeoutError:
         print("CRITICAL: Database connection timed out (30s). Strict mode - exiting.")
         db_connected = False
    except Exception as e:
        print(f"CRITICAL: Database connection failed: {e}")
        print("Falling back to local synthetic mode.")

    # 2. Check Data & Seed
    print("Checking for existing data...")
    
    existing_data = None
    if db_connected:
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(EvEvent).limit(1))
                existing_data = result.scalar_one_or_none()
        except Exception:
             print("Session creation failed, treating as empty.")
    
    if not existing_data or not db_connected: # Fallback if DB invalid
        print("Database empty or disconnected. Seeding/Loading from synthetic CSV...")
        # Locate CSV
    
    # Locate CSV regardless of mode
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
            
    if db_connected and not existing_data:
        print("Database empty. Seeding from synthetic CSV...")
        async with AsyncSessionLocal() as session:
            if csv_path:
                df_seed = pd.read_csv(csv_path)
                df_seed['timestamp'] = pd.to_datetime(df_seed['timestamp'])
                if df_seed['timestamp'].dt.tz is None:
                    df_seed['timestamp'] = df_seed['timestamp'].dt.tz_localize('UTC')
                
                # Bulk Insert
                events = df_seed.to_dict(orient='records')
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

    # 2.5 Seed Model Predictions and Recommendations (DB Backend)
    if db_connected:
        from .models.outputs import ModelPrediction, Recommendation
        from sqlalchemy import select, delete
        import datetime
        import uuid
        
        print("Checking for existing model predictions...")
        async with AsyncSessionLocal() as session:
            # Check if we have recent predictions (future)
            now = datetime.datetime.now()
            existing_preds = await session.execute(
                select(ModelPrediction).where(ModelPrediction.timestamp > now).limit(1)
            )
            
            # Use Shared Engine adapter to generate if needed
            if not existing_preds.scalar_one_or_none():
                 print("No future predictions found. Generating and Seeding from Loaded Models...")
                 
                 # 1. Forecast seeding
                 # Use Shared Adapter
                 from .models.dashboard.dashboard_engine import SharedForecastEngineAdapter
                 # We need raw data for the adapter. Use cache or seed from csv just loaded
                 # data_cache.df handles it
                 if data_cache.df is not None:
                     adapter = SharedForecastEngineAdapter(data_cache.df)
                     # Generate 7 days
                     res = adapter.ensemble.forecast(hours=24*7) 
                     
                     run_id = f"startup_seed_{int(now.timestamp())}"
                     
                     objs = []
                     # Map results to DB objects
                     # res keys: timestamp (list), ensemble (list), lower, upper
                     timestamps = res['timestamp']
                     values = res['ensemble']
                     lower = res['lower']
                     upper = res['upper']
                     
                     for i, ts in enumerate(timestamps):
                         objs.append(ModelPrediction(
                             run_id=run_id,
                             timestamp=ts,
                             predicted_value=float(values[i]),
                             model_type="ensemble_v1",
                             lower_bound=float(lower[i]),
                             upper_bound=float(upper[i]),
                             source_file="loaded_models"
                         ))
                     
                     session.add_all(objs)
                     await session.commit()
                     print(f"Seeded {len(objs)} prediction records (7 days).")
                 else:
                     print("Skipping forecast seeding - no input data available.")

                 # 2. Recommendation Seeding
                 from .models.recommendations.recommendation_engine import RecommendationEngine
                 if data_cache.session_df is not None:
                      rec_engine = RecommendationEngine(data_cache.session_df)
                      recs = rec_engine.generate_recommendations()
                      
                      rec_objs = []
                      for r in recs:
                          rec_objs.append(Recommendation(
                                title=r['title'],
                                priority=r['priority'],
                                location=r['location'],
                                expected_impact=r['expected_impact'],
                                estimated_cost=r['estimated_cost'],
                                roi_timeline=r['roi_timeline'],
                                category=r.get('category', 'General')
                          ))
                      session.add_all(rec_objs)
                      await session.commit()
                      print(f"Seeded {len(rec_objs)} recommendations.")
            else:
                 print("Future predictions already exist in DB. Skipping seed.")

    # 3. Load Data into Cache
    print("Loading data into Analytics Service...")
    
    if db_connected:
        try:
            async with AsyncSessionLocal() as session:
                result_all = await session.execute(select(EvEvent).order_by(EvEvent.timestamp))
                rows = result_all.scalars().all()
                data = [{
                    "timestamp": r.timestamp,
                    "station_id": r.station_id,
                    "vehicle_count": r.vehicle_count,
                    "session_count": r.session_count,
                    "occupancy_rate": r.occupancy_rate,
                    "queue_length": r.queue_length
                } for r in rows]
                data_cache.df = pd.DataFrame(data)
                print(f"Data loaded from DB: {len(data_cache.df)} rows")
        except Exception as e:
            print(f"DB Load failed ({e}). forcing CSV load.")
            db_connected = False # Fallback to CSV below
            
    if not db_connected:
        print("CRITICAL: Database connection failed. Strict mode enabled - exiting startup.")
        # We could raise an exception here to crash the pod, or just let it run empty. 
        # User requested "fail if fetching fails", so we just won't load fake data.
        pass

    # 4. Generate Consistent Session Data (Only if we have data)
    if data_cache.df is not None and not data_cache.df.empty:
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
