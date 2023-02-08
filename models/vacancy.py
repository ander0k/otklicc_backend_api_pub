from typing import TYPE_CHECKING
import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

from db.base_class import Base

if TYPE_CHECKING:
    from .app_user import AppUser  # noqa: F401

PUBLIC_ID_SERVER_DEFAULT_TEXT = sqlalchemy.sql.expression.text(
    "encode(digest(CAST(gen_random_uuid() as TEXT), 'sha256'), 'hex')"
)

class Vacancy(Base):
    """vacancy database table.
    модель таблицы вакансий
    sqlalchemy.ext.declarative
    """
    __tablename__ = 'v_vacancy'
    id = Column(postgres_dialect.UUID,primary_key=True,server_default=FetchedValue())
    title = Column(postgres_dialect.TEXT, nullable=False)
    code = Column(postgres_dialect.TEXT,unique=True,index=True,nullable=False, server_default=FetchedValue())
    experience = Column(postgres_dialect.INTEGER,comment='минимальный опыт в месяцах')
    post_date = Column(
        postgres_dialect.TIMESTAMP(timezone=True),
        comment='дата публикации вакансии - для управления временем появления '
                'вакансии в результатах поиска'
    )
    deadline = Column(postgres_dialect.DATE)
    leave_days = Column(postgres_dialect.INTEGER)
    left_days = Column(postgres_dialect.INTEGER)
    busyness = Column(
        postgres_dialect.INTEGER,
        comment='занятость ("полная", "частичная" и т.д.) - ссылка '
                'на справочник видов занятости'
    )
    view_count = Column(postgres_dialect.INTEGER, nullable=False)
    status = Column(postgres_dialect.SMALLINT,nullable=False, server_default=FetchedValue())
    professions = Column(postgres_dialect.TEXT,nullable=False)
    geos = Column(postgres_dialect.TEXT,nullable=False)
    salary_lo = Column(postgres_dialect.FLOAT)
    salary_hi = Column(postgres_dialect.FLOAT)
    currency = Column(
        postgres_dialect.TEXT,
        comment='зарплата: валюта, трехбуквенный код по справочнику ISO 4217'
    )
    term = Column(
        postgres_dialect.INTEGER,
        comment='зарплата: расчетный период (смена, неделя, месяц, год, проект и т.п.'
    )
    about = Column(postgres_dialect.TEXT)
    status_time = Column(
        postgres_dialect.TIMESTAMP(timezone=True),
        comment='дата-время перевода в текущий статус'
    )
    company = Column(postgres_dialect.TEXT)
    company_id = Column(
        postgres_dialect.UUID,
        nullable=False,
        comment='ссылка на компанию'
    )
    created = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,server_default=FetchedValue(),
        comment='[дата и] время создания записи'
    )
    updated = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,server_default=FetchedValue(),
        comment='[дата и] время изменения записи'
    )
    deleted = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,
        comment='признак и [дата и] время удаления записи, запись считается удалённой, если значение этого поля отлично от NULL'
    )
    last_db_user = Column(postgres_dialect.TEXT,nullable=True,server_default=FetchedValue(),
        comment='имя пользователя базы данных, внесшего последнее изменение записи'
    )
    last_app_user_id = Column(postgres_dialect.UUID,nullable=True,
        comment='ссылка на пользователя otklicc, последним изменившего запись'
    )

