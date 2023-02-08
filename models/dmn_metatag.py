import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from db.base_class import Base
from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship

PUBLIC_ID_SERVER_DEFAULT_TEXT = sqlalchemy.sql.expression.text(
    "encode(digest(CAST(gen_random_uuid() as TEXT), 'sha256'), 'hex')"
)


class Vcn_Demand(Base):
    """Datamodel for dmn_metatag
    модель таблицы метатэгов к требованиям вакансий
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
    demand_id = Column(
        postgres_dialect.UUID,
        nullable=False,
        comment='ссылка на требование'
    )
    text_value = Column(
        postgres_dialect.TEXT,
        nullable=False,
        comment='текстовое значение метатега (краткая запись сути требования)'
    )
    record_created = Column(
        postgres_dialect.TIMESTAMP(timezone=True),
        nullable=False,
        comment='[дата и] время создания записи'
    )
    record_updated = Column(
        postgres_dialect.TIMESTAMP(timezone=True),
        nullable=True,
        comment='[дата и] время создания записи - здесь измения записи будут '
                'запроещены'
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

    # Constraints
    # объявление уникального ключа на public_id сделано через Constraint, чтобы
    # иметь возможность задать возможность отложенной проверки (deferrable=True)
    # UniqueConstraint(
    #     ['public_id'], name='idxu_dmn_metatag_public_id', deferrable=True
    # )
    # ForeignKeyConstraint(
    #     'last_app_user_id', ['Application_User.internal_id'],
    #     use_alter=True, name='dmn_metatag_application_user_internal_id_fk',
    #     deferrable=True
    # )
    # ForeignKeyConstraint(
    #     'demand_id', ['Demand.internal_id'],
    #     use_alter=True, name='dmn_metatag_vcn_demand_internal_id_fk',
    #     deferrable=True
    # )
