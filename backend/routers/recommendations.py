from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.recommendation import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/")
def get_recommendations(db: Session = Depends(get_db)):
    recommendation = RecommendationService(db)
    # Return list directly as per frontend likely expectation (check api.js call)
    # api.js: getRecommendations: () => apiClient.get('/recommendations')
    # Service returns [{'title'..}..]
    return recommendation.generate_recommendations()

@router.post("/{id}/implement")
def implement_recommendation(id: str):
    return {"status": "success", "message": f"Recommendation {id} queued for implementation."}
