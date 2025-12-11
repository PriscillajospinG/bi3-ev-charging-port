# EV Charging Port Analytics & Optimization Suite

A comprehensive AI-driven solution for electric vehicle charging infrastructure. This project includes advanced demand forecasting and intelligent infrastructure optimization recommendations.

## 🚀 Key Features

### 1. Demand Prediction Engine (`analytics/`)
Accurate demand forecasting using a multi-model ensemble approach:
- **Models**: Facebook Prophet (Trend/Seasonality) + XGBoost (Event/Peak Detection) + LSTM (Sequence/Pattern Learning).
- **Capabilities**:
  - 24-hour and 7-day demand forecasts.
  - Peak demand detection with timestamps.
  - Confidence intervals and uncertainty bounds.
  - Real-time model accuracy evaluation using MAPE (Mean Absolute Percentage Error).

### 2. Recommendation Engine (`recommendations/`)
Actionable insights for infrastructure optimization:
- **Logic**: Rule-based analysis of station occupancy, queues, and revenue proxies.
- **Outputs**:
  - 6 specific infrastructure recommendations (e.g., "Add DC Fast Charger", "Relocate Unit").
  - Cost/Benefit analysis with ROI timelines.
  - Priority ranking (High/Medium/Low).
  - Confidence scores for each recommendation.

---

## 📂 Directory Structure

```
bi3-ev-charging-port/
├── analytics/                  # Demand Prediction Module
│   ├── demand_prediction_engine.py  # Main forecasting script
│   ├── demand_forecasting.ipynb     # Jupyter Notebook
│   ├── requirements.txt             # Dependencies
│   └── run.sh                       # Helper execution script
│
├── recommendations/            # Recommendation Module
│   ├── recommendation_engine.py     # Main optimization script
│   └── requirements.txt             # Dependencies
│
└── README.md                   # Project Documentation
```

---

## 🛠️ Usage Guide

### A. Run Demand Prediction
Generates demand forecasts and analytics reports.

1. **Navigate to analytics:**
   ```bash
   cd analytics
   ```
2. **Run (Automated):**
   ```bash
   ./run.sh
   ```
   *Note: `run.sh` automatically handles virtual environments and system library linking (libomp) for XGBoost.*

**Outputs:**
- `forecast_result.json`: Detailed JSON forecast.
- `forecast_plot.png`: Assessment visualization.

### B. Run Recommendations
Generates infrastructure optimization advice.

1. **Navigate to recommendations:**
   ```bash
   cd recommendations
   ```
2. **Run:**
   ```bash
   python3 -m venv venv && ./venv/bin/pip install -r requirements.txt && ./venv/bin/python recommendation_engine.py
   ```

**Outputs:**
- `recommendations.json`: Structured list of prioritized recommendations.

---

## 📊 Sample Outputs

**Forecast JSON (`forecast_result.json`):**
```json
{
  "forecast_24h": [12.5, 14.2, ...],
  "peak_demand": { "value": 37.5, "time": "2025-12-12 18:00" },
  "model_accuracy": "85.5%",
  "mobile_charger_recommendation": "Deploy... if occupancy > 80%"
}
```

**Recommendations JSON (`recommendations.json`):**
```json
{
  "summary": { "high_priority": 2, "estimated_revenue_lift": "$8.2K" },
  "recommendations": [
    {
      "title": "Add DC Fast Charger - Zone S01",
      "priority": "HIGH",
      "accuracy": "92%",
      "estimated_monthly_revenue": "$2,800"
    }
  ]
}
```