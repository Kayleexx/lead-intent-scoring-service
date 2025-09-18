from fastapi import APIRouter
from app.models.offer import Offer

router = APIRouter()

offers_db = []

@router.post("/offer")
def create_offer(offer: Offer):
    
    offers_db.append(offer.dict())
    return {"message": "Offer saved successfully!", "offer": offer}
