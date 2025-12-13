from fastapi import HTTPException
from .services.analytics import AnalyticsService
from .models.dashboard.dashboard_engine import DataSimulator
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import get_db
from .models.events import EvEvent
import datetime

# Singleton Cache (Simple in-memory for demo)
class DataCache:
    df = None
    session_df = None
    _service_instance = None

data_cache = DataCache()

def get_analytics_service():
    # Return cached service if available
    if data_cache._service_instance:
        return data_cache._service_instance

    # Only creating service if data is loaded, otherwise empty
    # In main startup we load data_cache
    if data_cache.df is None:
        # Fallback empty df to prevent crash if startup failed
        return AnalyticsService(pd.DataFrame({
            'timestamp': [], 
            'vehicle_count': [],
            'session_count': [],
            'occupancy_rate': [],
            'queue_length': []
        }))
    
    # Create and cache service
    service = AnalyticsService(data_cache.df, data_cache.session_df)
    # Pre-warm forecast to incur cost once (optional, but good)
    # service.get_forecast() 
    data_cache._service_instance = service
    return service
