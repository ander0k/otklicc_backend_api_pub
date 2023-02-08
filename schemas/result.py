from typing import Optional,List
from pydantic import BaseModel

class ResultDel(BaseModel):
    code: Optional[str]
    profile_code: Optional[str]

class ResultPut(ResultDel):
    content: Optional[str]


