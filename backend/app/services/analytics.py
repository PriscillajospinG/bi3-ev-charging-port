import pandas as pd
import numpy as np
import datetime
import random
from typing import List, Dict

# Import engines from the shared dashboard model
from ..models.dashboard.dashboard_engine import (
    RevenueEngine, OccupancyEngine, TrafficEngine, 
    AlertsEngine, PerformanceEngine, ForecastEngine,
    HeatmapEngine, WeeklyStatsEngine
)

class AnalyticsService:
    def __init__(self, data_frame: pd.DataFrame, session_df: pd.DataFrame = None):
        self.df = data_frame
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
        # Consistent session data (cached)
        self.session_df = session_df
        if self.session_df is not None:
            self.session_df['timestamp'] = pd.to_datetime(self.session_df['timestamp'])
            
        # Initialize Forecast Engine once to reuse
        self.forecast_engine = ForecastEngine(self.df)
        self.cached_forecast = None

    def get_latest_row(self):
        return self.df.iloc[-1]
        
    def get_forecast(self, days=7):
        # Cache forecast for performance in demo
        # In prod, cache with TTL
        if self.cached_forecast is None:
             self.cached_forecast = self.forecast_engine.generate(periods=24*days)
        return self.cached_forecast

    def get_revenue_panel(self):
        if self.session_df is None:
            return {} 
            
        engine = RevenueEngine(self.session_df)
        return engine.analyze()

    def get_live_occupancy(self):
        latest = self.get_latest_row()
        engine = OccupancyEngine(latest['occupancy_rate'], latest['queue_length'])
        return engine.get_status()

    def get_traffic_analysis(self):
        latest = self.get_latest_row()
        engine = TrafficEngine(latest['vehicle_count'])
        return engine.analyze()

    def get_alerts(self):
        latest = self.get_latest_row()
        occ_data = self.get_live_occupancy()
        
        # Use real forecast
        forecast = self.get_forecast(days=2) # Short term for alerts
        
        engine = AlertsEngine(occ_data, forecast, latest['queue_length'])
        return engine.check_alerts()

    def get_charger_overview(self):
        if self.session_df is None:
            return []
            
        engine = PerformanceEngine(self.session_df)
        return engine.get_table()

    def get_summary_metrics(self):
        table = self.get_charger_overview()
        
        if not table:
            return {}

        rev_sum = sum([float(c['revenue_24h'].replace('$','').replace(',','')) for c in table])
        sess_sum = sum([c['sessions_24h'] for c in table])
        
        return {
            "total_sessions": sess_sum,
            "total_revenue": f"${rev_sum:,.2f}",
            "avg_utilization": "74%", 
            "avg_performance": 94
        }
    
    def get_utilization_trend(self):
        # 24h trend
        latest_time = self.df['timestamp'].max()
        start_time = latest_time - datetime.timedelta(hours=24)
        subset = self.df[self.df['timestamp'] > start_time]
        
        trend = []
        for _, row in subset.iterrows():
            trend.append({
                "hour": row['timestamp'].strftime("%H:%00"),
                "utilization": int(row['occupancy_rate'] * 100)
            })
        return trend
        
    def get_heatmap(self):
        engine = HeatmapEngine(self.df)
        return engine.generate()
        
    def get_weekly_stats(self):
        engine = WeeklyStatsEngine(self.df)
        return engine.generate()
        
    def get_status_distribution(self):
        table = self.get_charger_overview()
        stat_counts = {"In Use": 0, "Available": 0, "Maintenance": 0, "Offline": 0}
        for c in table:
            s = c['status']
            if s in stat_counts:
                stat_counts[s] += 1
                
        total_c = 23
        return {
            "available": {"percent": int(stat_counts['Available']/total_c*100), "units": stat_counts['Available']},
            "occupied": {"percent": int(stat_counts['In Use']/total_c*100), "units": stat_counts['In Use']},
            "maintenance": {"percent": int(stat_counts['Maintenance']/total_c*100), "units": stat_counts['Maintenance']},
            "offline": {"percent": int(stat_counts['Offline']/total_c*100), "units": stat_counts['Offline']}
        }

    # --- Frontend Integration Methods ---
    
    def frontend_get_current_metrics(self):
        latest = self.get_latest_row()
        forecast = self.get_forecast()
        
        return {
            "currentQueue": int(latest['queue_length']),
            "queueChange": random.randint(-2, 5), # Still slightly dynamic as we lack historic queue diff in this simple View
            "vehiclesDetected": int(latest['vehicle_count']),
            "avgDwellTime": "23 min", 
            "dwellChange": 5,
            "peakPrediction": forecast['peak_hour'],
            "peakTime": forecast['peak_hour']
        }

    def frontend_get_chargers(self):
        # Map PerformanceEngine table to Frontend format
        table = self.get_charger_overview()
        chargers = []
        
        # Charger location map (fixed)
        zones = ["A", "B", "C"]
        
        for item in table:
            # item: {charger: 'C01', type, status, utilization, ...}
            c_id_str = item['charger'] # C01
            c_id = int(c_id_str[1:])
            
            # Deterministic location logic
            zone = zones[(c_id-1)//8] 
            bay = ((c_id-1)%8) + 1
            
            # Parse 'In Use' to 'occupied'
            status_map = {
                "In Use": "occupied",
                "Available": "available",
                "Maintenance": "maintenance",
                "Offline": "offline"
            }
            
            chargers.append({
                "id": c_id,
                "name": f"Charger {c_id_str}",
                "location": f"Zone {zone} - Bay {bay}",
                "status": status_map.get(item['status'], "offline"),
                "power": 150 if item['type'] == 'DC Fast' else 50,
                "type": item['type'],
                "sessionTime": item['avg_session'], 
                "energyDelivered": float(random.randint(10, 50)), # No live energy in table, sim
                "utilization": int(item['utilization'].replace('%','')),
                "sessions": item['sessions_24h'],
                "revenue": float(item['revenue_24h'].replace('$','').replace(',','')),
                "avgSession": int(item['avg_session'].split(' ')[0]),
                "performance": item['performance']
            })
        return chargers

    def frontend_get_utilization(self, range_val="24h"):
        trend = self.get_utilization_trend()
        return [{"time": t["hour"], "utilization": t["utilization"]} for t in trend]

    def frontend_get_occupancy(self):
        dist = self.get_status_distribution()
        return [
            {"name": "Available", "value": dist["available"]["units"]},
            {"name": "Occupied", "value": dist["occupied"]["units"]},
            {"name": "Maintenance", "value": dist["maintenance"]["units"]},
            {"name": "Offline", "value": dist["offline"]["units"]},
        ]
