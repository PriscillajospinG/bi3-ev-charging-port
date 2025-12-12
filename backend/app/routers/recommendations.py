from fastapi import APIRouter, Depends
from ..dependencies import get_analytics_service
from ..services.analytics import AnalyticsService
from ..models.recommendations.recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/")
async def get_recommendations(service: AnalyticsService = Depends(get_analytics_service)):
    # Initialize Engine with REAL session data
    if service.session_df is None:
        return []
    
    engine = RecommendationEngine(service.session_df)
    results = engine.generate_recommendations()
    return results
