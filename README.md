# EV Charging Port Analytics & Optimization Suite

A comprehensive AI-driven solution for electric vehicle charging infrastructure. This project integrates advanced demand forecasting, detailed infrastructure recommendations, and a robust backend logic layer for analytics dashboards.

## 🚀 Key Modules

### 1. Demand Prediction Engine (`backend_models/prediction/`)
Accurate demand forecasting using a multi-model ensemble approach.
- **Models**: Prophet (Trend), XGBoost (Events), LSTM (Sequences).
- **Features**: 24h/7d forecasts, peak detection, confidence intervals, and MAPE accuracy evaluation.

### 2. Recommendation Engine (`backend_models/recommendations/`)
Actionable insights for infrastructure optimization.
- **Logic**: Rule-based analysis of utilization, queues, and revenue.
- **Outputs**: Prioritized recommendations (e.g., "Add Charger", "Optimize Layout") with ROI and confidence scores.

### 3. Analytics Backend Layer (`backend_models/analytics/`)
The core logic powering the user-facing Analytics Dashboard.
- **Metrics**: Real-time calculation of Utilization, Sessions, Energy, and Revenue (with % change).
- **Forecasting**: Internal ensemble model for dashboard predictions.
- **Structure**: Generates the exact JSON schema required by the UI.

---

## 📂 Directory Structure

```
bi3-ev-charging-port/
├── backend_models/
│   ├── prediction/             # Standalone Demand Prediction
│   │   ├── demand_prediction_engine.py
│   │   └── run.sh
│   │
│   ├── recommendations/        # Recommendation Engine
│   │   ├── recommendation_engine.py
│   │   └── recommendations.json
│   │
│   └── analytics/              # Dashboard Backend Logic
│       ├── analytics_backend.py
│       ├── analytics_dashboard.json
│       └── run_with_libomp.sh
│
└── README.md                   # Project Documentation
```

---

## 🛠️ Usage Guide

### A. Run Demand Prediction
```bash
cd backend_models/prediction
./run.sh
```
**Output:** `forecast_result.json`, `forecast_plot.png`

### B. Run Recommendations
```bash
cd backend_models/recommendations
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
./venv/bin/python recommendation_engine.py
```
**Output:** `recommendations.json` (Includes confidence accuracy scores)

### C. Run Analytics Backend
```bash
cd backend_models/analytics
./run_with_libomp.sh
```
**Output:** 
- `analytics_dashboard.json`: Complete dashboard data.
- `forecast_result.json`: Backend internal forecast check.

---

## 📊 Sample Data

**Dashboard Structure (`analytics_dashboard.json`):**
```json
{
  "summary": {
    "avg_utilization": "74.2%",
    "revenue": "$3,847",
    "revenue_change": "+8.7%"
  },
  "daily_trend": [ ... ],
  "status_distribution": { "available": { "percent": 52 } }
}
```