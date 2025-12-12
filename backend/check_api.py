import requests
import sys

def check(url):
    print(f"Checking {url}...")
    try:
        r = requests.get(url, timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                print(f"Data: List with {len(data)} items")
                print(f"Sample: {data[0] if data else 'Empty'}")
            elif isinstance(data, dict):
                print(f"Data: Dict with keys {list(data.keys())}")
                if 'forecast' in data:
                    print(f"Forecast keys: {list(data['forecast'].keys())}")
            else:
                print(f"Data type: {type(data)}")
        else:
            print(f"Error Content: {r.text[:200]}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    check("http://localhost:8000/")
    check("http://localhost:8000/api/recommendations/")
    check("http://localhost:8000/api/forecast/run")
