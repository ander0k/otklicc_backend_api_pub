from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

class VacancyCard(BaseModel):
    title       : Optional[str] = None
    code        : Optional[str] = None
    experience  : Optional[int] = None
    post_date   : Optional[datetime] = None
    leave_days  : Optional[int] = None
    left_days   : Optional[int] = None
    busyness    : Optional[int] = None
    view_count  : Optional[int] = None
    salary_lo   : Optional[int] = None
    salary_hi   : Optional[int] = None
    currency    : Optional[str] = None
    term        : Optional[int] = None


class CompanyCard(BaseModel):
    name        : Optional[str] = None
    code        : Optional[str] = None
    logo_image  : Optional[str] = None
    color       : Optional[str] = None
    sec_color   : Optional[str] = None
    status      : Optional[int] = None
    verified    : Optional[bool] = None
    owner_email : Optional[str] = None
    comp_viewer_list: Optional[dict] = None

class Feed(BaseModel):
    company_card: Optional[CompanyCard]
    vacancy_card: Optional[VacancyCard]
    cus_status  : Optional[int]
    status      : Optional[int]
    vac_owner_list : Optional[dict] = None
    vac_viewer_list: Optional[dict] = None
    geos        : Optional[List[str]] = None
    applies     : Optional[int]

