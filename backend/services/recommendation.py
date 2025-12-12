import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def generate_recommendations(self):
        query = text("SELECT avg(occupancy_rate) as occ, max(queue_length) as queue FROM vehicle_metrics")
        try:
            res = self.db.execute(query).fetchone()
            avg_occ = res[0] if res and res[0] is not None else 0
            max_q = res[1] if res and res[1] is not None else 0
        except:
            avg_occ, max_q = 0, 0
        
        # Normalize if percent
        if avg_occ > 1: avg_occ /= 100
        
        recs = []
        
        if avg_occ > 0.7:
             recs.append({
                "title": "Deploy Mobile Charging Unit",
                "priority": "HIGH",
                "category": "Capacity",
                "reason": f"Heigh occupancy ({avg_occ*100:.1f}%) detected."
             })
        elif avg_occ < 0.3:
             recs.append({
                "title": "Launch Promotional Campaign",
                "priority": "MEDIUM",
                "category": "Marketing",
                "reason": f"Underutilization ({avg_occ*100:.1f}%) detected."
             })
             
        if max_q > 5:
             recs.append({
                "title": "Optimize Entrance Flow",
                "priority": "HIGH",
                "category": "Operations",
                "reason": f"Max queue length of {max_q} vehicles."
             })

        if not recs:
             recs.append({
                 "title": "Maintain Standard Operations",
                 "priority": "LOW",
                 "category": "Status",
                 "reason": "Metrics are within normal ranges."
             })

        return recs
