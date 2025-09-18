from fastapi import FastAPI
from app.routes import offer

# Initialize FastAPI app
app = FastAPI(
    title="Lead Intent Scoring Service",
    description="Backend service to score leads based on product/offer context + AI reasoning.",
    version="1.0.0"
)

# Register routers (keeps routes modular)
app.include_router(offer.router, tags=["Offers"])

# Root endpoint (for health check or quick test)
@app.get("/")
def root():
    return {"message": "Hello, Backend Engineer 🚀"}
