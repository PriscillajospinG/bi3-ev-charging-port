from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

# --- Dashboard Schemas ---

class RevenuePanel(BaseModel):
    today: Dict[str, Any]
    week: Dict[str, Any]
    month: Dict[str, Any]

class LiveOccupancy(BaseModel):
    occupancy_percent: int
    status: str
    total_chargers: int
    in_use: int
    available: int
    waiting: int
    avg_wait_time: str

class TrafficAnalysis(BaseModel):
    approaching: int
    eta_avg: int
    routes: List[Dict[str, Any]]

class Alert(BaseModel):
    title: str
    timestamp: str
    details: str
    location: str

class ChargerOverview(BaseModel):
    charger: str
    type: str
    status: str
    utilization: str
    sessions_24h: int
    revenue_24h: str
    avg_session: str
    performance: int

class SummaryMetrics(BaseModel):
    total_sessions: int
    total_revenue: str
    avg_utilization: str
    avg_performance: int

class UtilizationPoint(BaseModel):
    hour: str
    utilization: int

class StatusDistribution(BaseModel):
    available: Dict[str, int]
    occupied: Dict[str, int]
    maintenance: Dict[str, int]
    offline: Dict[str, int]

class DashboardResponse(BaseModel):
    revenue_panel: RevenuePanel
    live_occupancy: LiveOccupancy
    traffic_analysis: TrafficAnalysis
    alerts: List[Alert]
    charger_overview: List[ChargerOverview]
    summary_metrics: SummaryMetrics
    utilization_trend: List[UtilizationPoint]
    status_distribution: StatusDistribution
    forecast_summary: Optional[Dict[str, Any]] = None

# --- Forecast Schemas ---

class ForecastResponse(BaseModel):
    timestamp: List[str]
    prophet: List[float]
    lstm: List[float]
    xgboost: List[float]
    ensemble: List[float]
    lower: List[float]
    upper: List[float]
    model_accuracy: str

# --- Recommendation Schemas ---

class Recommendation(BaseModel):
    title: str
    priority: str
    location: str
    expected_impact: str
    estimated_cost: str

# --- Frontend Integration Schemas ---

class FrontendMetrics(BaseModel):
    currentQueue: int
    queueChange: int
    vehiclesDetected: int
    avgDwellTime: str
    dwellChange: int
    peakPrediction: str
    peakTime: str

class FrontendCharger(BaseModel):
    id: int
    name: str
    location: str
    status: str
    power: int
    type: str
    sessionTime: str
    energyDelivered: float
    utilization: int
    sessions: int
    revenue: float
    avgSession: int
    performance: int

class FrontendOccupancyItem(BaseModel):
    name: str
    value: int

class FrontendUtilizationItem(BaseModel):
    time: str
    utilization: int

