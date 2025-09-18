import csv
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Lead
import app.schemas as schemas
from typing import List

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a CSV file of leads and save to DB.
    Expected columns: name,role,company,industry,location,linkedin_bio
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

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
            linkedin_bio=row["linkedin_bio"],
        )
        db.add(lead)
        leads_added += 1

    db.commit()

    return {"message": f"Uploaded {leads_added} leads successfully!"}


@router.get("/leads", response_model=List[schemas.LeadOut])
def get_leads(db: Session = Depends(get_db)):
    """
    Fetch all leads from DB.
    """
    return db.query(models.Lead).all()
