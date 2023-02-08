"""
Описание модели валидации компании (company)
"""
from typing import Optional,List
from pydantic import BaseModel, HttpUrl

STATUS_DRAFT   = 10  # черновик
STATUS_MODER   = 20  # на модерации
STATUS_REJECT  = 30  # отклонена
STATUS_PUBLIC  = 40  # опубликована
STATUS_ARCHIVE = 50  # в архиве

# Shared properties

class Company_Base(BaseModel):
    """
    Компания (организация)
    """
    status: Optional[int] = None # STATUS_xxx
    name: Optional[str] = None
    logo_image: Optional[HttpUrl] = None
    thumbnail_image: Optional[HttpUrl] = None
    color: Optional[str] = None
    sec_color: Optional[str] = None
    about: Optional[str] = None
    sub_name: Optional[str] = None
    synonyms: Optional[str] = None


class CompanyDel(BaseModel):
    code: Optional[str] = None
    comp_viewer_list: Optional[List[str]]


class CompanyBase(Company_Base):
    code: Optional[str] = None
    owner_email: Optional[str] = None
    owner_name: Optional[str] = None


class CompanyRd(CompanyBase):
    verified: Optional[bool] = None


class CompanyWr(CompanyBase):
    verified: Optional[bool] = None
    owner_user_id: Optional[str] = None


class CompanyPut(CompanyBase):
    verified: Optional[bool] = None
    owner_email: Optional[str] = None
    comp_viewer_list: Optional[List[str]] = None


class CompanyPost(Company_Base):
    status: Optional[int] = STATUS_DRAFT
    comp_viewer_list: Optional[List[str]] = None


class CompanyOwned(CompanyBase):
    owner_email: Optional[str] = None
    comp_viewer_list: Optional[dict] = None

# Properties to receive on item creation
class CompanyCreate(CompanyWr):
    id: Optional[str]
    pass


# Properties to receive on item update
class CompanyUpdate(CompanyBase):
    id: Optional[str]
    pass


# Properties shared by models stored in DB
class CompanyInDBBase(CompanyBase):
    id: Optional[str]
    class Config:
        orm_mode = True


# Properties to return to client
class Company(CompanyInDBBase):
    pass


# Properties stored in DB
class CompanyInDB(CompanyInDBBase):
    id: Optional[str]
    pass
