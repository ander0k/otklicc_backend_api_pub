"""
Описание модели валидации требования из вакансий (vcn_demand)
"""
from typing import Optional, List

from uuid import UUID

from pydantic import BaseModel, Field
from .dmn_metatag import DmnMetatagInDB

# Shared properties
class VcnDemandBase(BaseModel):
    """
    Требования из вакансий
    """
    public_id: UUID = Field(
        description='публичный (постоянный) уникальный идентификатор записи'
    )
    vacancy_id: UUID = Field(
        description='ссылка на вакансию'
    )
    position_number: int = Field(
        description='номер требования (по порядку)'
    )
    wording: str = Field(
        description='формулировка требования'

    )
    value_rate: float = Field(
        default=1.0,        
        description='ценность, рейтинг, коэффициент, вес, значимость'
    )
    metatags: List[DmnMetatagInDB] = Field(
        default=None,
        description='метатэги'
    )


# Properties to receive on item creation
class VcnDemandCreate(VcnDemandBase):
#    title: str
    pass


# Properties to receive on item update
class VcnDemandUpdate(VcnDemandBase):
    pass


# Properties shared by models stored in DB
class VcnDemandInDBBase(VcnDemandBase):
    class Config:
        orm_mode = True


# Properties to return to client
class VcnDemand(VcnDemandInDBBase):
    pass


# Properties properties stored in DB
class VcnDemandInDB(VcnDemandInDBBase):
    pass
