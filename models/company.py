import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from db.base_class import Base
from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

PUBLIC_ID_SERVER_DEFAULT_TEXT = sqlalchemy.sql.expression.text(
    "encode(digest(CAST(gen_random_uuid() as TEXT), 'sha256'), 'hex')"
)


class Company(Base):
    """Datamodel for Company
    модель таблицы компаний (организаций)
    """
    __tablename__ = 'v_company'
    id = Column(postgres_dialect.UUID,primary_key=True,server_default=FetchedValue())
    code = Column(postgres_dialect.TEXT,unique=True,index=True,nullable=False, server_default=FetchedValue())
    status = Column(postgres_dialect.SMALLINT,nullable=False, server_default=FetchedValue())
    name = Column(postgres_dialect.TEXT,nullable=False,comment='название (общеизвестное)')
    sub_name = Column(postgres_dialect.TEXT,nullable=True)
    synonyms = Column(postgres_dialect.TEXT,nullable=True)
    verified = Column(postgres_dialect.BOOLEAN,nullable=False,server_default=FetchedValue())
    color = Column(postgres_dialect.TEXT,comment='фирменный цвет hex (#00FFFF)')
    sec_color = Column(postgres_dialect.TEXT)
    logo_image = Column(postgres_dialect.TEXT,comment='ссылка на логотип')
    thumbnail_image = Column(postgres_dialect.TEXT)
    about = Column(postgres_dialect.TEXT,nullable=True)
    owner_email = Column(postgres_dialect.TEXT,nullable=True)
    owner_name = Column(postgres_dialect.TEXT,nullable=True)
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
    owner_user_id = Column(postgres_dialect.UUID,nullable=True,server_default=FetchedValue())

    # Constraints
    # объявление уникального ключа на public_id сделано через Constraint, чтобы
    # иметь возможность задать возможность отложенной проверки (deferrable=True)
    # UniqueConstraint(
    #     ['public_id'], name='idxu_Company_public_id', deferrable=True
    # )
    # ForeignKeyConstraint(
    #     'last_app_user_id', ['Application_User.internal_id'],
    #     use_alter=True, name='company_application_user_internal_id_fk',
    #     deferrable=True
    # )
    # ForeignKeyConstraint(
    #     'geolocation_id', ['Geolocation.internal_id'],
    #     use_alter=True, name='company_geolocation_internal_id_fk',
    #     deferrable=True
    # )
    #
    # # Indexes
    # Index('idx_company_last_app_user_id', 'last_app_user_id')
    # Index('idx_company_is_active', 'is_active')
    #
    # # Relationships
    # users = relationship('Application_User', back_populates='company')
    # last_app_user = relationship(
    #     "Application_User",
    #     foreign_keys="Company.last_app_user_id"
    # )
    # geolocation = relationship('Geolocation', back_populates='company')

