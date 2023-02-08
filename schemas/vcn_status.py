"""
Описание модели валидации статусов (состояний) вакансий (vcn_status)
"""

from typing import Optional

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


# Shared properties
class VcnStatusBase(BaseModel):
    """
    статус (состояние) вакансии ("черновик", "опубликована", "в архиве")
    """
    code: int = Field(
        description='уникальный идентификатор записи (код статуса)'
    )
    display_label: str = Field(
        description='название (расшифровка кода)'
    )
    description: Optional[str] = Field(
        default=None,
        description='описание, дополнительная информация'
    )


# Properties to receive on item creation
class VcnStatusCreate(VcnStatusBase):
#    title: str
    pass


# Properties to receive on item update
class VcnStatusUpdate(VcnStatusBase):
    pass


# Properties shared by models stored in DB
class VcnStatusInDBBase(VcnStatusBase):
    class Config:
        orm_mode = True


# Properties to return to client
class VcnStatus(VcnStatusInDBBase):
    pass


# Properties properties stored in DB
class VcnStatusInDB(VcnStatusInDBBase):
    pass
