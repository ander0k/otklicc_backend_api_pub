from typing import Optional
from pydantic import BaseModel, HttpUrl, EmailStr


class AppUserBase(BaseModel):
    utype: Optional[str] = None
    img: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    notifications: Optional[int] = None
    about: Optional[str] = None


class AppUserComm(AppUserBase):
    code: Optional[str] = None


class AppUserCreate(AppUserComm):
    email: EmailStr
    password: str


class AppUserUpdate(AppUserComm):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    prof_view: Optional[int] = None
    reqr_view: Optional[bool] = None
    comp_view: Optional[bool] = None
    notifications: Optional[int] = None
    educations: Optional[str] = None
    jobs: Optional[str] = None


class AppUserInDBBase(AppUserComm):
    id: Optional[str] = None
    class Config:
        orm_mode = True


class AppUser(AppUserComm):
    pass


class AppUserInDB(AppUserComm):
    passkey: str


