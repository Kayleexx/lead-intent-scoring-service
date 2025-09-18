from sqlalchemy import Column, Integer, String
from app.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    company = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    location = Column(String, nullable=False)
    linkedin_bio = Column(String, nullable=False)
