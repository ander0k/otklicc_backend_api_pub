
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

class FavDel(BaseModel):
    name                : Optional[str] = None

class FavOut(FavDel):
    apply_time          : Optional[datetime] = None
    professions         : Optional[str] = None
    parent_professions  : Optional[str] = None
    company             : Optional[str] = None
    parent_company      : Optional[str] = None
    geos                : Optional[str] = None
    parent_geos         : Optional[str] = None
    experience          : Optional[str] = None
    deadline            : Optional[bool] = None
    popular             : Optional[bool] = None

class FavPut(FavOut):
    owner : Optional[UUID] = None
