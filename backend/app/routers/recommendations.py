from fastapi import APIRouter, Depends
from ..dependencies import get_rec_service
from ..services.recommendations import RecommendationService
from ..schemas.dashboard import Recommendation
from typing import List

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/", response_model=List[Recommendation])
async def get_recommendations(service: RecommendationService = Depends(get_rec_service)):
    return service.get_recommendations()
