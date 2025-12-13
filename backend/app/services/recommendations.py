import random
from typing import List, Dict

class RecommendationService:
    def get_recommendations(self) -> List[Dict]:
        """
        Generates intelligent EV infrastructure recommendations.
        """
        recommendations = [
            {
                "title": "Add Fast Charger",
                "priority": "HIGH",
                "location": "Zone A (Downtown)",
                "expected_impact": "+24% Revenue",
                "estimated_cost": "$45,000",
                "roi_timeline": "14 Months",
                "key_insights": [
                    "Queue length > 4 often",
                    "Utilization > 90% peak"
                ]
            },
            {
                "title": "Deploy Mobile Charging Unit",
                "priority": "MEDIUM",
                "location": "Zone C (Event Center)",
                "expected_impact": "Reduce Wait Time by 15%",
                "estimated_cost": "$2,000 / month",
                "roi_timeline": "Immediate",
                "key_insights": [
                    "Weekend spikes detected",
                    "Events correlate with overflow"
                ]
            },
            {
                "title": "Upgrade to Ultra-Fast",
                "priority": "LOW",
                "location": "Station S02",
                "expected_impact": "+10% Throughput",
                "estimated_cost": "$80,000",
                "roi_timeline": "24 Months",
                "key_insights": [
                    "Current avg session 45min",
                     "Users requesting faster speeds"
                ]
            }
        ]
        
        # Dynamic element (shuffle or optional extras)
        if random.random() > 0.8:
            recommendations.append({
                 "title": "Relocate Underused Charger",
                 "priority": "MEDIUM",
                 "location": "Station S05",
                 "expected_impact": "Optimization",
                 "estimated_cost": "$5,000",
                 "roi_timeline": "6 Months",
                 "key_insights": ["Utilization < 10%"]
            })
            
        return recommendations
