from pydantic import BaseModel
from typing import List, Optional

# Response schema for leads
class LeadOut(BaseModel):
    id: int
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: str

    class Config:
        orm_mode = True  # allows returning SQLAlchemy models directly
