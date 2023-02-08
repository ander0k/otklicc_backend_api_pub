"""
Описание модели валидации расчетных периодов зарплат:
  смена, неделя, месяц, год, проект и т.п. (salary_term)
"""

from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class SalaryTermBase(BaseModel):
    """
    статус (состояние) вакансии ("черновик", "опубликована", "в архиве")
    """
    code: int = Field(
        description='уникальный идентификатор записи (код)'
    )
    display_label: str = Field(
        description='название (расшифровка кода)'
    )
    description: Optional[str] = Field(
        default=None,
        description='описание, дополнительная информация'
    )


# Properties to receive on item creation
class SalaryTermCreate(SalaryTermBase):
    pass


# Properties to receive on item update
class SalaryTermUpdate(SalaryTermBase):
    pass


# Properties shared by models stored in DB
class SalaryTermInDBBase(SalaryTermBase):
    class Config:
        orm_mode = True


# Properties to return to client
class SalaryTerm(SalaryTermInDBBase):
    pass


# Properties properties stored in DB
class SalaryTermInDB(SalaryTermInDBBase):
    pass
