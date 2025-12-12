from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import test_connection
from backend.routers import dashboard, analytics, predictions, recommendations, detection

app = FastAPI(title="EV Charging Station Analytics", version="1.0.0")

# CORS Setup
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
    "*" # Allow all for dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    test_connection()

# Mount routers matching frontend's expect base: /api
app.include_router(dashboard.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(detection.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to EV Charging Analytics API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
