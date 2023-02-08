import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from db.base_class import Base
from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship

PUBLIC_ID_SERVER_DEFAULT_TEXT = sqlalchemy.sql.expression.text(
    "encode(digest(CAST(gen_random_uuid() as TEXT), 'sha256'), 'hex')"
)


class Salary_Term(Base):
    """Datamodel for Salary_Term
    модель таблицы справочника расчетных периодов зарплат
    """
    internal_id = Column(
        postgres_dialect.UUID,
        # дефолтное значение генерится на сервере gen_random_uuid()
        server_default=sqlalchemy.schema.FetchedValue(),
        primary_key=True,
        comment='внутренний (скрытый) уникальный идентификатор записи'
    )
    public_id = Column(
        postgres_dialect.TEXT,
        # значение может быть автоматически сгенерировано на сервере,
        # либо определено при вставке (или изменении) - для сохранения
        # постоянного значения
        server_default=PUBLIC_ID_SERVER_DEFAULT_TEXT,
        nullable=False,
        comment='публичный (постоянный) уникальный идентификатор записи'
    )
    record_created = Column(
        postgres_dialect.TIMESTAMP(timezone=True),
        nullable=False,
        comment='[дата и] время создания записи'
    )
    record_updated = Column(
        postgres_dialect.TIMESTAMP(timezone=True),
        nullable=True,
        comment='[дата и] время изменения записи'
    )
    record_deleted = Column(
        postgres_dialect.TIMESTAMP(timezone=True),
        nullable=True,
        comment='признак и [дата и] время удаления записи, запись считается '
                'удалённой, если значение этого поля отлично от NULL'
    )
    last_db_user = Column(
        postgres_dialect.TEXT,
        server_default=sqlalchemy.sql.expression.text('current_user'),
        nullable=True,
        comment='имя пользователя базы данных, внесшего последнее изменение '
                'записи'
    )
    last_app_user_id = Column(
        postgres_dialect.UUID,
        server_default=sqlalchemy.sql.expression.text('NULL'),
        comment='ссылка на пользователя otklicc, последним изменившего запись'
    )
    display_label = Column(
        postgres_dialect.TEXT,
        nullable=False,
        comment='период (смена, неделя, месяц, год, проект и т.п.)'
    )
    description = Column(
        postgres_dialect.TEXT,
        comment='описание, дополнительная информация'
    )

    # Constraints
    # объявление уникального ключа на public_id сделано через Constraint, чтобы
    # иметь возможность задать возможность отложенной проверки (deferrable=True)
    # UniqueConstraint(
    #     ['public_id'], name='idxu_salary_term_public_id', deferrable=True
    # )
    # ForeignKeyConstraint(
    #     'last_app_user_id', ['Application_User.internal_id'],
    #     use_alter=True, name='company_application_user_internal_id_fk',
    #     deferrable=True
    # )
    #
    # # Indexes
    # Index('idx_Company_last_app_user_id', 'last_app_user_id')
    #
    # # Relationships
    # last_app_user = relationship(
    #     "Application_User",
    #     foreign_keys="Vacancy.last_app_user_id"
    # )
    # company = relationship('Company', back_populates='company')
    #
