"""
Описание модели валидации графиков работы
(work_schedule)
"""

from typing import Optional

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


# Shared properties
class WorkScheduleBase(BaseModel):
    """
    график работы (гибкий, сменный, 30 часов в неделю, вахтовый... и т.п.)
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
class WorkScheduleCreate(WorkScheduleBase):
#    title: str
    pass


# Properties to receive on item update
class WorkScheduleUpdate(WorkScheduleBase):
    pass


# Properties shared by models stored in DB
class WorkScheduleInDBBase(WorkScheduleBase):
    class Config:
        orm_mode = True


# Properties to return to client
class WorkSchedule(WorkScheduleInDBBase):
    pass


# Properties properties stored in DB
class WorkScheduleInDB(WorkScheduleInDBBase):
    pass
