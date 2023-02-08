from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

STATUS_DRAFT   = 10  # черновик
STATUS_MODER   = 20  # на модерации
STATUS_REJECT  = 30  # отклонена
STATUS_PUBLIC  = 40  # опубликована
STATUS_ARCHIVE = 50  # в архиве


# Shared properties
class Vacancy_Base(BaseModel):
    title       : Optional[str] = None
    status      : Optional[int] = None
    experience  : Optional[int] = None
    leave_days  : Optional[int] = None
    busyness    : Optional[int] = None
    salary_lo   : Optional[int] = None
    salary_hi   : Optional[int] = None
    currency    : Optional[str] = None
    term        : Optional[int] = None


class VacancyBase(Vacancy_Base):
    about       : Optional[str] = None


class VacancyCardPost(VacancyBase):
    professions : Optional[List[str]] = None
    geos        : Optional[List[str]] = None

class VacancySearch(Vacancy_Base):
    code        : Optional[str] = None
    post_date   : Optional[datetime] = None
    deadline    : Optional[date] = None
    left_days   : Optional[int] = None
    view_count  : Optional[int] = None


class VacancyCard(VacancySearch):
    about       : Optional[str] = None


class CompanyCard(BaseModel):
    name        : Optional[str] = None
    code        : Optional[str] = None
    logo_image  : Optional[str] = None
    color       : Optional[str] = None
    sec_color   : Optional[str] = None
    status      : Optional[int] = None
    verified    : Optional[bool] = None


class VacancyData(BaseModel):
    terms       : Optional[dict] = None
    cus_status  : Optional[int] = None
    requirements: Optional[dict] = None
    responses   : Optional[dict] = None


class VacancyDataIn(BaseModel):
    demands     : Optional[List[str]] = None
    terms       : Optional[List[str]] = None
    vac_owner_list : Optional[List[str]] = None
    vac_viewer_list: Optional[List[str]] = None


class VacancyDel(VacancyDataIn):
    code        : Optional[str] = None
    destroy_all : Optional[bool] = False
    responses   : Optional[List[str]] = None
    professions : Optional[List[str]] = None
    geos        : Optional[List[str]] = None


class VacancyCusPut(BaseModel):
    cus_status  : Optional[int] = None
    terms       : Optional[dict] = None
    demands     : Optional[dict] = None
    responses   : Optional[dict] = None
    metatags    : Optional[dict] = None


class VacancyGet(BaseModel):
    company_card: Optional[CompanyCard] = None
    vacancy_card: Optional[VacancyCard] = None


class VacancyPost(BaseModel):
    comp_code   : str = None
    vacancy_card: VacancyBase
    demands     : Optional[List[str]] = None
    terms       : Optional[List[str]] = None
    professions : Optional[List[str]] = None
    geos        : Optional[List[str]] = None
    vac_owner_list : Optional[List[str]] = None
    vac_viewer_list: Optional[List[str]] = None


class VacancyAnyPut(BaseModel):
    email       : Optional[str] = None
    responses   : Optional[dict] = None


class VacancyPut(BaseModel):
    code: str = None
    vacancy_card: Optional[VacancyBase]
    bookmarked  : Optional[bool] = None
    responses   : Optional[dict] = None
    metatags    : Optional[dict] = None
    coefficients: Optional[dict] = None
    demands     : Optional[dict] = None
    terms       : Optional[dict] = None
    professions : Optional[List[str]] = None
    geos        : Optional[List[str]] = None
    vac_owner_list : Optional[List[str]] = None
    vac_viewer_list: Optional[List[str]] = None


# Properties to receive on vacancy creation
class VacancyCreate(VacancyBase):
    company_id  : Optional[UUID] = None


class VacancyUpdInfo(BaseModel):
    vac_owner_list : Optional[str] = None
    vac_viewer_list: Optional[str] = None

class VacancyGetInfo(BaseModel):
    view_count     : Optional[int] = None
    vac_owner_list : Optional[List[str]] = None
    vac_viewer_list: Optional[List[str]] = None


class VacancyNewInfo(VacancyUpdInfo):
    code  : Optional[str] = None
    title : Optional[str] = None


# Properties to receive on vacancy update
class VacancyUpdate(VacancyBase):
    id          : Optional[str] = None
    code        : Optional[str] = None


# Properties shared by models stored in DB
class VacancyInDBBase(VacancyBase):
    class Config:
        orm_mode = True


# Properties to return to client
class Vacancy(VacancyInDBBase):
    pass


# Properties properties stored in DB
class VacancyInDB(VacancyInDBBase):
    pass
