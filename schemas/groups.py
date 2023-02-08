"""
Описание модели валидации компании (company)
"""
from typing import Optional,List
from pydantic import BaseModel
from enum import Enum

class Child(BaseModel):
    child_val: Optional[str] = None
    code: Optional[str] = None
    syn: Optional[str] = None


class Group_Item(BaseModel):
    parent_val: Optional[str] = None
    child_val: Optional[str] = None

class Group_Base(BaseModel):
    """
    Группы значений
    """
    items: Optional[List[Group_Item]] = None

class Group(Group_Base):
    pass

class TreeName(str, Enum):
    geos = "geos"
    tags = "metatags"
    profs = "profession"
    companies = "companies"

class GroupPost(BaseModel):
    group: Optional[str] = None
    parent_val: Optional[str] = None
    child_val: Optional[str] = None
    syn: Optional[str] = None

class GroupDel(BaseModel):
    group: Optional[str] = None
    parent: Optional[str] = None
    child: Optional[str] = None

class GroupPut(GroupDel):
    new_name: Optional[str] = None
