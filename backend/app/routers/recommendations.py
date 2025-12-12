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
    # Try fetching from DB first
    from sqlalchemy import select
    
    # Get latest recommendations (limit 50)
    result = await db.execute(select(Recommendation).order_by(Recommendation.generated_at.desc()).limit(50))
    rows = result.scalars().all()
    
    if rows:
        # Convert to list of dicts matching frontend expectation
        return [{
            "title": r.title,
            "priority": r.priority,
            "location": r.location,
            "expected_impact": r.expected_impact,
            "estimated_cost": r.estimated_cost,
            "roi_timeline": r.roi_timeline,
            "category": r.category,
            # Add other fields if needed or mocks
        } for r in rows]

    # Fallback to Engine Generation if DB empty
    if service.session_df is None:
        return []
    
    engine = RecommendationEngine(service.session_df)
    results = engine.generate_recommendations()
    
    # Persist Recommendations
    for r in results:
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
