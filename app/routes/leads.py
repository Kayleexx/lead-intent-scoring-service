import csv
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

router = APIRouter()
leads_db: List[dict] = []

@router.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...)):
    """
    Upload a CSV file of leads.
    Expected columns: name,role,company,industry,location,linkedin_bio
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()

    reader = csv.DictReader(decoded)
    required_fields = ["name", "role", "company", "industry", "location", "linkedin_bio"]

    for row in reader:
        # Ensure all required fields exist
        if not all(field in row for field in required_fields):
            raise HTTPException(status_code=400, detail="CSV missing required fields")
        leads_db.append(row)

    return {"message": f"Uploaded {len(leads_db)} leads successfully!"}
