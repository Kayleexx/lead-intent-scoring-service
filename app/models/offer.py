from pydantic import BaseModel
from typing import List

class Offer(BaseModel):
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]
