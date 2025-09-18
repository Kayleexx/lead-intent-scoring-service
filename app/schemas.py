from pydantic import BaseModel

class LeadOut(BaseModel):
    id: int
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: str

    class Config:
        orm_mode = True
