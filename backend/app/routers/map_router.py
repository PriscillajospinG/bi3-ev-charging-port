from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..etl.api_map import fetch_open_charge_map_data

router = APIRouter(prefix="/api/map", tags=["Map"])

@router.get("/stations", response_model=List[dict])
async def get_stations(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    distance: float = 50,
    country_code: str = "IN",
    limit: int = 100
):
    """
    Get charging stations from Open Charge Map.
    Defaults to India (country_code='IN') if no coordinates provided.
    """
    try:
        stations = await fetch_open_charge_map_data(
            latitude=lat,
            longitude=lng,
            distance=distance,
            country_code=country_code,
            max_results=limit
        )
        return stations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
