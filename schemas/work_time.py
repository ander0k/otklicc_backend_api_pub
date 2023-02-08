"""
Описание модели валидации режимов занятости (полная, частичная, временная)
(work_time)
"""

from typing import Optional

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


# Shared properties
class WorkTimeBase(BaseModel):
    """
    режим занятости (полная, частичная, временная)
    """
    public_id: UUID = Field(
        description='публичный (постоянный) уникальный идентификатор записи'
    )
    display_label: str = Field(
        description='название (расшифровка кода)'
    )
    description: Optional[str] = Field(
        default=None,
        description='описание, дополнительная информация'
    )


# Properties to receive on item creation
class WorkTimeCreate(WorkTimeBase):
#    title: str
    pass


# Properties to receive on item update
class WorkTimeUpdate(WorkTimeBase):
    pass


# Properties shared by models stored in DB
class WorkTimeInDBBase(WorkTimeBase):
    class Config:
        orm_mode = True


# Properties to return to client
class WorkTime(WorkTimeInDBBase):
    pass


# Properties properties stored in DB
class WorkTimeInDB(WorkTimeInDBBase):
    pass
