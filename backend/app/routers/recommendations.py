from fastapi import APIRouter, Depends
from ..dependencies import get_analytics_service
from ..services.analytics import AnalyticsService
from ..models.recommendations.recommendation_engine import RecommendationEngine

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.outputs import Recommendation

@router.get("/")
async def get_recommendations(
    service: AnalyticsService = Depends(get_analytics_service),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Engine with REAL session data
    if service.session_df is None:
        return []
    
    engine = RecommendationEngine(service.session_df)
    results = engine.generate_recommendations()
    
    # Persist Recommendations
    # This might slow down valid "GET" requests if we save every time. 
    # Usually we'd have a separate "POST /generate" or check if recent ones exist.
    # For this task "push all model outputs... into new tables", we will save them on generation.
    
    for r in results:
        # Check if identical title/location exists recently? For now, just insert all for history.
        rec_db = Recommendation(
            title=r['title'],
            priority=r['priority'],
            location=r['location'],
            expected_impact=r['expected_impact'],
            estimated_cost=r['estimated_cost'],
            roi_timeline=r['roi_timeline'],
            category=r.get('category', 'General')
        )
        db.add(rec_db)
    
    await db.commit()
    
    return results
