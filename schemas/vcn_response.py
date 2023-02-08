"""
Описание модели валидации откликов на требования из вакансий (response)
"""
from typing import Optional, List

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

# Shared properties
class VcnResponseBase(BaseModel):
    """
    Отклики на требования из вакансий
    """
    public_id: UUID = Field(
        description='публичный (постоянный) уникальный идентификатор записи'
    )
    demand_id: UUID = Field(
        description='ссылка на требование вакансии'
    )
    candidate_user_id: UUID = Field(
        description='ссылка на откликнувшегося кандидата'
    )
    content: str = Field(description='формулировка отклика')
    scored_timestamp: Optional[datetime] = Field(
        default=None,
        description='когда установлена оценка'
    )
    scored_mark: Optional[int] = Field(
        default=None,
        description='выставленная оценка'
    )
    scored_user_id: UUID = Field(
        description='ссылка на откликнувшегося кандидата'
    )
    record_created: datetime = Field(
        description='[дата и] время создания записи'
    )
    record_updated: Optional[datetime] = Field(
        default_factory=datetime.now,
        description='[дата и] время изменения записи'
    )
    record_deleted: Optional[datetime] = Field(
        default=None,
        description='признак и [дата и] время удаления записи, запись '
                    'считается удалённой, если значение этого поля '
                    'отлично от NULL'
    )
    last_db_user: Optional[str] = Field(
        description='имя пользователя базы данных, последним изменившего запись'
    )
    last_app_user_id: UUID = Field(
        description='ссылка на пользователя, кто это сделал'
    )


# Properties to receive on item creation
class VcnResponseCreate(VcnResponseBase):
    pass


# Properties to receive on item update
class VcnResponseUpdate(VcnResponseBase):
    pass


# Properties shared by models stored in DB
class VcnResponseInDBBase(VcnResponseBase):
    class Config:
        orm_mode = True


# Properties to return to client
class VcnResponse(VcnResponseInDBBase):
    pass

# Properties to receive on vcnresponse update
class VcnResponseUpdate(VcnResponseBase):
    pass


# Properties properties stored in DB
class VcnResponseInDB(VcnResponseInDBBase):
    pass
