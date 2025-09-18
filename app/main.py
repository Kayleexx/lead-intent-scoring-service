from fastapi import FastAPI
from app.database import engine, Base
import app.models  # Import models so tables are registered
from app.routes import leads
from dotenv import load_dotenv
load_dotenv()


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lead Intent Scoring Service",
    description="Backend service to score leads based on product/offer context + AI reasoning.",
    version="1.0.0"
)

# Register routes
app.include_router(leads.router, tags=["Leads"])

@app.get("/")
def root():
    return {"message": "Hello world"}
