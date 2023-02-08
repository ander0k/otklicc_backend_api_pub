from typing import Optional
from pydantic import BaseModel


class CronConfig(BaseModel):
    recom_period: Optional[int]
    recom_working: Optional[bool]
    dedline_hour: Optional[int]
    dedline_working: Optional[bool]
    garbage_hour: Optional[int]
    garbage_working: Optional[bool]
