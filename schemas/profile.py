import json
from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl
from .app_user import AppUserBase


class ProfileBase(AppUserBase):
    prof_view: Optional[int] = None
    education: Optional[dict] = None
    job: Optional[dict] = None


class ProfileCUS(ProfileBase):
    reqr_view: Optional[bool] = None
    skills: Optional[dict] = None


class ProfileHR(ProfileBase):
    comp_view: Optional[bool] = None
    comp_viewer_list: Optional[dict] = None
    vac_owner_list: Optional[dict] = None
    vac_viewer_list: Optional[dict] = None


class Profile(ProfileCUS, ProfileHR):
    pass


class ProfilePut(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    img: Optional[HttpUrl] = None
    about: Optional[str] = None
    prof_view: Optional[int] = None
    reqr_view: Optional[bool] = None
    comp_view: Optional[bool] = None
    notifications: Optional[int] = None
    phone: Optional[str] = None
    education: Optional[dict] = None
    job: Optional[dict] = None


class ProfileDel(BaseModel):
    delete_acc: bool = None
    job: Optional[List[str]] = None
    education: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    comp_viewer_list: Optional[List[str]] = None
    vac_owner_list : Optional[List[str]] = None
    vac_viewer_list: Optional[List[str]] = None

# class ProfileUpdate(ProfileBase):
#     pass
