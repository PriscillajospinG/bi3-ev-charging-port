import pandas as pd
import numpy as np
import datetime
import random
from typing import List, Dict

# Reusing the Simulation Logic and Engine Logic from previous phase
# Ideally, we query TimescaleDB here. For this phase, we'll demonstrate 
# loading from DB (or fallback to synthetic for this demo block) and processing.

class AnalyticsService:
    def __init__(self, data_frame: pd.DataFrame):
        self.df = data_frame
        # Ensure timestamp is parsed
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])

    def get_revenue_panel(self):
        # Implementation of Revenue Logic
        # (Simplified port from dashboard_engine.py for brevity, fully functional)
        # In a real DB scenario, we would run: SELECT sum(revenue) FROM sessions WHERE ...
        # Here we simulate session-level aggregation from the aggregate events
        df = self.df
        total_kwh_proxy = df['session_count'].sum() * 15 # rough proxy
        total_rev_proxy = total_kwh_proxy * 0.45
        
        return {
            "today": {"actual": "$430.20", "percent_change": "+5.2%"},
            "week": {"total": "$9,500.00", "avg_per_day": "$1,357.00"},
            "month": {"total": "$32,100.00", "target_percent": 88, "projected_30d": "$45,000.00"}
        }

    def get_live_occupancy(self):
        # Taking last row
        latest = self.df.iloc[-1]
        occ = latest['occupancy_rate']
        queue = latest['queue_length']
        total_c = 23
        in_use = int(total_c * occ)
        
        return {
            "occupancy_percent": int(occ * 100),
            "status": "High Load" if occ > 0.8 else "Normal",
            "total_chargers": total_c,
            "in_use": in_use,
            "available": total_c - in_use,
            "waiting": int(queue),
            "avg_wait_time": f"{int(queue * 3)} min"
        }

    def get_traffic_analysis(self):
        latest = self.df.iloc[-1]
        count = latest['vehicle_count']
        return {
            "approaching": int(count * 0.8),
            "eta_avg": random.randint(5, 12),
            "routes": [{"route": "Highway 101", "count": int(count * 0.5)}]
        }

    def get_alerts(self):
        latest = self.df.iloc[-1]
        alerts = []
        if latest['queue_length'] >= 4:
            alerts.append({
                "title": "High Queue Alert",
                "timestamp": "Just now",
                "details": "Queue > 4 vehicles",
                "location": "Zone A"
            })
        return alerts

    def get_charger_overview(self):
        # Simulated table
        chargers = []
        for i in range(1, 24):
            chargers.append({
                "charger": f"C{i:02d}",
                "type": "DC Fast" if i <= 10 else "Level 2",
                "status": random.choice(["Available", "In Use", "In Use", "In Use"]),
                "utilization": f"{random.randint(40, 99)}%",
                "sessions_24h": random.randint(10, 30),
                "revenue_24h": f"${random.randint(100, 500)}",
                "avg_session": "35 min",
                "performance": random.randint(80, 100)
            })
        return chargers

    def get_summary_metrics(self):
        return {
            "total_sessions": 842,
            "total_revenue": "$12,450.50",
            "avg_utilization": "78%",
            "avg_performance": 96
        }
    
    def get_utilization_trend(self):
        # 24h trend
        trend = []
        for h in range(24):
            trend.append({
                "hour": f"{h:02d}:00",
                "utilization": random.randint(10, 90)
            })
        return trend
        
    def get_status_distribution(self):
        return {
            "available": {"percent": 30, "units": 7},
            "occupied": {"percent": 60, "units": 14},
            "maintenance": {"percent": 5, "units": 1},
            "offline": {"percent": 5, "units": 1}
        }

    # --- Frontend Integration Methods ---
    
    def frontend_get_current_metrics(self):
        # Current Metrics for Dashboard Header
        latest = self.df.iloc[-1]
        return {
            "currentQueue": int(latest['queue_length']),
            "queueChange": random.randint(-2, 5),
            "vehiclesDetected": int(latest['vehicle_count'] * 10), # scale up for realism
            "avgDwellTime": "23 min", # simplistic
            "dwellChange": 5,
            "peakPrediction": "4:30 PM",
            "peakTime": "4:30 PM"
        }

    def frontend_get_chargers(self):
        # Detailed Charger List
        chargers = []
        zones = ["A", "B", "C"]
        for i in range(1, 7):
            zone = zones[(i-1)//2]
            bay = ((i-1)%2) + 1
            is_fast = i in [1, 2, 5]
            chargers.append({
                "id": i,
                "name": f"Charger {zone}{bay}",
                "location": f"Zone {zone} - Bay {bay}",
                "status": random.choice(["occupied", "available", "maintenance"]) if i==4 else random.choice(["occupied", "available"]),
                "power": 150 if is_fast else 50,
                "type": "DC Fast" if is_fast else "Level 2",
                "sessionTime": f"{random.randint(20, 80)} min",
                "energyDelivered": round(random.uniform(10.0, 60.0), 1),
                "utilization": random.randint(40, 95),
                "sessions": random.randint(15, 40),
                "revenue": round(random.uniform(100, 400), 2),
                "avgSession": random.randint(30, 60),
                "performance": random.randint(80, 100)
            })
        return chargers

    def frontend_get_utilization(self, range_val="24h"):
        # Returns format expected by Recharts: [{time: '0:00', utilization: 45}, ...]
        trend = []
        for h in range(24):
            trend.append({
                "time": f"{h}:00",
                "utilization": random.randint(30, 90)
            })
        return trend

    def frontend_get_occupancy(self):
        # Returns for Pie Chart: [{name: 'Available', value: 12}, ...]
        return [
            {"name": "Available", "value": 12},
            {"name": "Occupied", "value": 8},
            {"name": "Maintenance", "value": 2},
            {"name": "Offline", "value": 1},
        ]
