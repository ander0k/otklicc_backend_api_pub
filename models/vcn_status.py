from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as postgres_dialect

from db.base_class import Base

if TYPE_CHECKING:
    from .app_user import AppUser  # noqa: F401


class Vcn_Status(Base):
    """vcn_status database table.
    модель таблицы статусов (состояний) вакансий
    sqlalchemy.ext.declarative
    """

    code = Column(
        postgres_dialect.INTEGER,
        primary_key=True,
        index=True,
        comment='уникальный идентификатор записи (код статуса)'
    )
    is_active = Column(
        postgres_dialect.BOOLEAN,
        server_default=sqlalchemy.sql.expression.text('True'),
        comment='признак активен/неактивен, пользователям для выбора '
                'из списка значений доступны только записи с is_active == True'
    )
    display_label = Column(
        postgres_dialect.TEXT,
        nullable=False,
        comment='название (расшифровка кода)'
    )
    description = Column(
        postgres_dialect.TEXT,
        comment='описание, дополнительная информация о статусе'
    )
