import pandas as pd
from sqlalchemy.orm import Session
from backend.database import engine
from sqlalchemy import text
import datetime
import random 

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_data(self, window: str = "24h") -> pd.DataFrame:
        """Fetch data from TimescaleDB based on window."""
        now = datetime.datetime.now()
        
        if window == '24h':
            start_time = now - datetime.timedelta(hours=24)
        elif window == '7d':
            start_time = now - datetime.timedelta(days=7)
        elif window == '30d':
            start_time = now - datetime.timedelta(days=30)
        else:
            start_time = now - datetime.timedelta(hours=24)

        query = text("""
            SELECT 
                timestamp,
                vehicle_count,
                session_count,
                occupancy_rate,
                queue_length
            FROM vehicle_metrics
            WHERE timestamp >= :start_time
            ORDER BY timestamp ASC
        """)
        
        try:
            result = self.db.execute(query, {"start_time": start_time})
            rows = result.fetchall()
        except Exception as e:
            print(f"DB Error: {e}")
            return pd.DataFrame()
        
        if not rows:
             return pd.DataFrame()

        df = pd.DataFrame(rows, columns=['timestamp', 'vehicle_count', 'session_count', 'occupancy_rate', 'queue_length'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    def compute_metrics(self, window="24h"):
        df = self.get_data(window)
        if df.empty:
             return {
                "avg_utilization": "0%",
                "utilization_change": "0%",
                "total_sessions": 0,
                "sessions_change": "0%",
                "energy_delivered_kWh": 0,
                "revenue": "$0",
                "revenue_change": "0%"
            }

        # Calculate metrics
        curr_util = df['occupancy_rate'].mean() # Rate is 0-1
        # Normalize if percentage was stored
        if curr_util > 1: curr_util = curr_util / 100 
        
        curr_sess = df['session_count'].sum()
        
        curr_energy = curr_sess * 6.2
        curr_rev = curr_energy * 0.45
        
        return {
            "avg_utilization": f"{curr_util*100:.1f}%",
            "utilization_change": "+0%", # Placeholder
            "total_sessions": int(curr_sess),
            "sessions_change": "+0%",
            "energy_delivered_kWh": int(curr_energy),
            "revenue": f"${curr_rev:,.0f}",
            "revenue_change": "+0%"
        }

    def get_daily_utilization_trend(self, window="24h"):
        df = self.get_data(window)
        if df.empty: return []

        if window == '24h':
            resample_rule = '1H'
        else:
             resample_rule = '1D'
             
        hourly = df.set_index('timestamp').resample(resample_rule)['occupancy_rate'].mean().reset_index()
        hourly['occupancy_rate'] = hourly['occupancy_rate'].fillna(0)
        
        trend = []
        for _, row in hourly.tail(30).iterrows(): 
            ts = row['timestamp']
            label = ts.strftime("%H:%M") if window == '24h' else ts.strftime("%a")
            # Normalize display
            val = row['occupancy_rate']
            if val <= 1.0: val *= 100
            
            trend.append({
                "time": label,
                "value": int(val) 
            })
        return trend
