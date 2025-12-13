import asyncio
import json
import datetime
import uuid
import sys
import os

# Add app to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import AsyncSessionLocal
from app.models.outputs import ModelPrediction, Recommendation

async def import_data():
    print("--- Importing JSON Data to Database ---")
    
    async with AsyncSessionLocal() as session:
        # 1. Import Recommendations
        try:
            with open('app/models/recommendations/recommendations.json', 'r') as f:
                rec_data = json.load(f)
                
            count_rec = 0
            for r in rec_data.get('recommendations', []):
                rec_db = Recommendation(
                    title=r.get('title'),
                    priority=r.get('priority'),
                    location=r.get('location'),
                    expected_impact=r.get('expected_impact'),
                    estimated_cost=r.get('estimated_cost'),
                    roi_timeline=r.get('roi_timeline'),
                    category=r.get('category', 'General')
                )
                session.add(rec_db)
                count_rec += 1
            print(f"Queued {count_rec} recommendations.")
        except FileNotFoundError:
            print("Warning: recommendations.json not found.")

        # 2. Import Forecast
        try:
            with open('app/models/prediction/forecast_result.json', 'r') as f:
                forecast_data = json.load(f)
            
            run_id = str(uuid.uuid4())
            # forecast_7d is a list of values. We assume they start from now, hourly.
            values = forecast_data.get('forecast_7d', [])
            start_time = datetime.datetime.now()
            
            count_pred = 0
            for i, val in enumerate(values):
                ts = start_time + datetime.timedelta(hours=i)
                # Lower/Upper bounds not in simple list, mock them slightly for visualization
                # or use value itself if no bound.
                l_bound = val * 0.9
                u_bound = val * 1.1
                
                pred = ModelPrediction(
                    run_id=run_id,
                    timestamp=ts,
                    predicted_value=float(val),
                    model_type='ensemble_json_import',
                    lower_bound=l_bound,
                    upper_bound=u_bound
                )
                session.add(pred)
                count_pred += 1
            print(f"Queued {count_pred} predictions.")
            
        except FileNotFoundError:
            print("Warning: forecast_result.json not found.")

        # 3. Commit
        await session.commit()
        print("Data successfully committed to database.")

if __name__ == "__main__":
    asyncio.run(import_data())
