"""
Описание модели валидации метатэгов к требованиям вакансий (vcn_demand)
"""

from typing import Optional

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


# Shared properties
class DmnMetatagBase(BaseModel):
    """
    метатэги к требованиям вакансий
    """
    public_id: UUID = Field(
        description='публичный (постоянный) уникальный идентификатор записи'
    )
    demand_id: UUID = Field(
        description='ссылка на требование'
    )
    text_value: str = Field(
        description='текстовое значение метатега (краткая запись сути '
                    'требования)'

    )
    record_created: datetime = Field(
        description='[дата и] время создания записи'
    )
    record_deleted: Optional[datetime] = Field(
        default=None,
        description='признак и [дата и] время удаления записи, запись '
                    'считается удалённой, если значение этого поля '
                    'отлично от NULL'
    )
    last_app_user_id: UUID = Field(
        description='ссылка на пользователя, кто это сделал'
    )


# Properties to receive on item creation
class DmnMetatagCreate(DmnMetatagBase):
#    title: str
    pass


# Properties to receive on item update
class DmnMetatagUpdate(DmnMetatagBase):
    pass


# Properties shared by models stored in DB
class DmnMetatagInDBBase(DmnMetatagBase):
    class Config:
        orm_mode = True


# Properties to return to client
class DmnMetatag(DmnMetatagInDBBase):
    pass


# Properties properties stored in DB
class DmnMetatagInDB(DmnMetatagInDBBase):
    pass
