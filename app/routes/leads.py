import csv
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Lead
from app.schemas import LeadOut
from typing import List
import os
import requests  # for Gemini API

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In-memory store for current offer
current_offer = {}

# --- Upload leads ---
@router.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")
    
    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    required_fields = ["name", "role", "company", "industry", "location", "linkedin_bio"]
    leads_added = 0

    for row in reader:
        if not all(field in row for field in required_fields):
            raise HTTPException(status_code=400, detail="CSV missing required fields")
        
        lead = Lead(
            name=row["name"],
            role=row["role"],
            company=row["company"],
            industry=row["industry"],
            location=row["location"],
            linkedin_bio=row["linkedin_bio"]
        )
        db.add(lead)
        leads_added += 1

    db.commit()
    return {"message": f"Uploaded {leads_added} leads successfully!"}


# --- Set current offer ---
@router.post("/offer")
async def set_offer(offer: dict):
    global current_offer
    current_offer = offer
    return {"message": "Offer saved successfully!", "offer": current_offer}


# --- Score leads ---
@router.post("/score")
def score_leads(db: Session = Depends(get_db)):
    global current_offer
    if not current_offer:
        raise HTTPException(status_code=400, detail="No offer uploaded")

    leads = db.query(Lead).all()
    scored_leads = []

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_URL = "https://api.gemini.com/v1/complete"  # Example endpoint; replace with real

    for lead in leads:
        # --- Rule-based scoring ---
        rule_score = 0

        role_lower = lead.role.lower()
        if any(x in role_lower for x in ["head", "manager", "director", "vp"]):
            rule_score += 20
        elif any(x in role_lower for x in ["coordinator", "specialist", "analyst"]):
            rule_score += 10

        if lead.industry.lower() in [x.lower() for x in current_offer.get("ideal_use_cases", [])]:
            rule_score += 20
        else:
            rule_score += 0

        data_complete = all([lead.name, lead.role, lead.company, lead.industry, lead.location, lead.linkedin_bio])
        if data_complete:
            rule_score += 10

        # --- AI scoring (Gemini) ---
        ai_points = 0
        reasoning = ""
        try:
            prompt = f"""
            Classify the buying intent (High/Medium/Low) for this lead:
            Lead: {lead.name}, Role: {lead.role}, Company: {lead.company}, Industry: {lead.industry}, Location: {lead.location}, Bio: {lead.linkedin_bio}
            Offer: {current_offer}
            Explain reasoning in 1-2 sentences.
            """
            headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
            response = requests.post(GEMINI_API_URL, json={"prompt": prompt})
            result = response.json()
            intent = result.get("intent", "Medium")
            reasoning = result.get("reasoning", "")
            ai_points = {"High":50, "Medium":30, "Low":10}.get(intent, 30)
        except Exception as e:
            reasoning = f"AI scoring failed: {str(e)}"
            ai_points = 0

        total_score = rule_score + ai_points
        scored_leads.append({
            "name": lead.name,
            "role": lead.role,
            "company": lead.company,
            "intent": intent,
            "score": total_score,
            "reasoning": reasoning
        })

    return {"message": f"Scored {len(scored_leads)} leads successfully!", "results": scored_leads}
