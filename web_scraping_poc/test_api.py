import requests
import json

API_KEY = "daeddd31-1f19-49f7-b2f2-274391e866ef"
BASE_URL = "https://api.openchargemap.io/v3/poi"

def get_open_charge_map_data():
    headers = {
        "User-Agent": "EVChargingPort/1.0",
        "Content-Type": "application/json"
    }
    
    params = {
        "key": API_KEY,
        "countrycode": "IN",  # Filter for India
        "maxresults": 5,  # Limit to 5 results to see structure
        "compact": True,  # Use compact=True to reduce size, or False to see full details
        "verbose": False
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        print(json.dumps(data, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    get_open_charge_map_data()
