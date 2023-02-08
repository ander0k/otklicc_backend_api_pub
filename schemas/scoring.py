from typing import Optional,List
from pydantic import BaseModel
from uuid import UUID

class ScoringPut(BaseModel):
    demand: Optional[UUID]
    profile_code: Optional[str]
    grade: Optional[int]


