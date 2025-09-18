from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import offer, leads

app = FastAPI(
    title="Lead Intent Scoring Service",
    description="Backend service to score leads based on product/offer context + AI reasoning.",
    version="1.0.0"
)

app.include_router(offer.router, tags=["Offers"])
app.include_router(leads.router, tags=["Leads"])

@app.get("/")
def root():
    return {"message": "Hello world"}
