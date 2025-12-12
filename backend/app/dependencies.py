from fastapi import HTTPException
from .services.analytics import AnalyticsService
from .services.forecast import PredictionService
from .services.recommendations import RecommendationService

# Global Data Cache (Simulating DB load for this phase)
class DataCache:
    df = None
    session_df = None
    
data_cache = DataCache()

def get_analytics_service():
    if data_cache.df is None:
        raise HTTPException(status_code=503, detail="Data not loaded yet")
    # Init service with both raw events and detailed session data
    return AnalyticsService(data_cache.df, data_cache.session_df)

def get_prediction_service():
    return PredictionService()

def get_rec_service():
    return RecommendationService()
