import requests
import json
import pandas as pd
from tabulate import tabulate

API_BASE_URL = "http://localhost:8005/api"

def fetch_and_display(endpoint, title):
    url = f"{API_BASE_URL}{endpoint}"
    print(f"\n{'='*50}")
    print(f"Fetching {title} from: {url}")
    print(f"{'='*50}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                # Pretty print list of objects (like trend data)
                df = pd.DataFrame(data)
                print(tabulate(df, headers='keys', tablefmt='psql'))
            elif isinstance(data, dict):
                # Pretty print dictionary (like specific stats)
                print(json.dumps(data, indent=4))
            else:
                print(data)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    print("Fetching Analytics Data from Backend...")
    
    # 1. Utilization Trend
    fetch_and_display("/analytics/utilization?window=24h", "Utilization Trend (24h)")
    
    # 2. Traffic Data
    fetch_and_display("/analytics/traffic?window=24h", "Traffic Data (24h)")
    
    # 3. Occupancy Stats
    fetch_and_display("/analytics/occupancy", "Occupancy Stats")
    
    # 4. Heatmap Data
    fetch_and_display("/analytics/heatmap", "Heatmap Data")

    print("\n\nData Source Information:")
    print("-" * 30)
    print("These endpoints fetch data via 'AnalyticsService' in 'backend/services/analytics.py'.")
    print("The service queries the 'vehicle_metrics' table in your TimescaleDB.")
