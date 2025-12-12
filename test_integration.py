import requests
import json
import sys

BASE_URL = "http://localhost:8005/api"

def test_health():
    try:
        r = requests.get("http://localhost:8005/health")
        print(f"Health Check: {r.status_code} {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False

def test_endpoints():
    endpoints = [
        "/dashboard/stats",
        "/chargers/status",
        "/analytics/utilization",
        "/predictions/demand",
        "/recommendations/"
    ]
    
    success = True
    for ep in endpoints:
        try:
            url = f"{BASE_URL}{ep}"
            print(f"Testing {url}...", end=" ")
            r = requests.get(url)
            if r.status_code == 200:
                print("✅ OK")
                # print(json.dumps(r.json(), indent=2))
            else:
                print(f"❌ Failed ({r.status_code})")
                print(r.text)
                success = False
        except Exception as e:
            print(f"❌ Error: {e}")
            success = False
    return success

if __name__ == "__main__":
    if test_health():
        test_endpoints()
    else:
        print("Backend not reachable.")
