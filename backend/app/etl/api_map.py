import httpx
import asyncio
from typing import List, Dict, Any, Optional

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPEN_CHARGE_MAP_API_KEY")
BASE_URL = "https://api.openchargemap.io/v3/poi"

async def fetch_open_charge_map_data(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    distance: float = 10,
    distance_unit: str = "KM",
    country_code: str = "IN",
    max_results: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetches charging station data from Open Charge Map API.
    
    Args:
        latitude: Latitude of the center point (optional)
        longitude: Longitude of the center point (optional)
        distance: Radius to search
        country_code: ISO Country Code (e.g., 'IN' for India, 'US' for USA)
        max_results: Maximum number of results to return
    
    Returns:
        List of charging stations
    """
    params = {
        "output": "json",
        "countrycode": country_code,
        "maxresults": max_results,
        "key": API_KEY,
        "compact": True,
        "verbose": False
    }

    if latitude is not None and longitude is not None:
        params["latitude"] = latitude
        params["longitude"] = longitude
        params["distance"] = distance
        params["distanceunit"] = distance_unit
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

if __name__ == "__main__":
    # Test run
    # Example: Fetching for India (no specific lat/long to get country-wide top results)
    
    async def main():
        print(f"Fetching stations in India...")
        stations = await fetch_open_charge_map_data(country_code="IN", max_results=5)
        print(f"Found {len(stations)} stations.")
        for s in stations:
            print(f"- {s.get('AddressInfo', {}).get('Title')} ({s.get('AddressInfo', {}).get('Town')})")
            
    asyncio.run(main())
