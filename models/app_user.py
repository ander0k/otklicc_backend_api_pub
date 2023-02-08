import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from sqlalchemy.sql.expression import true
from db.base_class import Base
from sqlalchemy import sql,Column,ForeignKeyConstraint,UniqueConstraint,Index
from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import text as sqltext
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

PUBLIC_ID_SERVER_DEFAULT_TEXT = sqlalchemy.sql.expression.text(
    "encode(digest(CAST(gen_random_uuid() as TEXT), 'sha256'), 'hex')"
)


# зарегистрированные пользователи otklicc
class AppUser(Base):
    """Datamodel for app_user
    модель таблицы зарегистрированных пользователей otklicc
    """
    __tablename__ = 'app_user'
    id = Column(postgres_dialect.UUID,primary_key=True,server_default=FetchedValue(),
        comment='идентификатор записи'
    )
#    actual_start = Column(postgres_dialect.TIMESTAMP,nullable=False,server_default=FetchedValue(),
    actual_start = Column(postgres_dialect.TIMESTAMP,nullable=True,server_default=FetchedValue(),
        comment='исторические данные (timetravel): время начала действия (актуальности)'
    )
    actual_end = Column(postgres_dialect.TIMESTAMP,nullable=False,#True,
        comment='исторические данные (timetravel): время завершения действия (актуальности), null - для актуальных, действующих'
    )
#    created = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=False,server_default=FetchedValue(),
    created = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,server_default=FetchedValue(),
        comment='[дата и] время создания записи'
    )
    updated = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,server_default=FetchedValue(),
        comment='[дата и] время изменения записи'
    )
    deleted = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,
        comment='признак и [дата и] время удаления записи, запись считается удалённой, если значение этого поля отлично от NULL'
    )
#    last_db_user = Column(postgres_dialect.TEXT,nullable=False,server_default=FetchedValue(),
    last_db_user = Column(postgres_dialect.TEXT,nullable=True,server_default=FetchedValue(),
        comment='имя пользователя базы данных, внесшего последнее изменение записи'
    )
    last_app_user_id = Column(postgres_dialect.UUID,nullable=True,
        comment='ссылка на пользователя otklicc, последним изменившего запись'
    )
    passkey = Column(postgres_dialect.TEXT,nullable=False,
        comment='хэш (соленый) пароля'
    )
    company_id = Column(postgres_dialect.UUID,
        comment='ссылка на компанию пользователя'
    )
    is_active = Column(postgres_dialect.BOOLEAN,nullable=False,server_default=FetchedValue(),
        comment='признак активированного (с возможностью подключения) пользователя (активирован, если is_active==True)'
    )
    
    code = Column(postgres_dialect.TEXT,unique=True,index=True,nullable=False, server_default=FetchedValue())
    utype = Column(postgres_dialect.TEXT, nullable=True, server_default=FetchedValue())
    img = Column(postgres_dialect.TEXT,comment='имя файла (hash) картинки, фото')
    first_name = Column(postgres_dialect.TEXT,comment='имя')
    last_name = Column(postgres_dialect.TEXT,comment='фамилия')
    email = Column(postgres_dialect.TEXT,nullable=False,unique=True,comment='адрес email - обязательный, уникальный')
    phone = Column(postgres_dialect.TEXT,nullable=True,comment='телефон')
    about = Column(postgres_dialect.TEXT,nullable=True,comment='о себе')
    prof_view = Column(postgres_dialect.SMALLINT,nullable=False, server_default=FetchedValue())
    reqr_view = Column(postgres_dialect.BOOLEAN,nullable=False, server_default=FetchedValue())
    comp_view = Column(postgres_dialect.BOOLEAN,nullable=False, server_default=FetchedValue())
    notifications = Column(postgres_dialect.SMALLINT,nullable=False, server_default=FetchedValue())
    educations = Column(postgres_dialect.TEXT,nullable=True,comment='')
    jobs = Column(postgres_dialect.TEXT,nullable=True,comment='')
    
    def is_adm(self) -> bool:
        return self.utype == 'ADM'

    # Constraints
    # объявление уникального ключа на public_id сделано через Constraint, чтобы
    # иметь возможность задать возможность отложенной проверки (deferrable=True)
    #UniqueConstraint(
    #    ['public_id'], name='idxu_application_user_public_id', deferrable=True
    #)
    # объявление внешнего ключа на last_app_user_id сделано через Constraint,
    # чтобы иметь возможность задать возможность отложенной проверки
    # (deferrable=True)
    # ForeignKeyConstraint(
    #     'last_app_user_id', ['application_user.internal_id'],
    #     use_alter=True, name='application_user_application_user_internal_id_fk',
    #     deferrable=True
    # )
    # ForeignKeyConstraint(
    #     'company_id', ['company.company_id'],
    #     use_alter=True, name='application_user_company_id_fk',
    #     deferrable=True
    # )

    # Indexes
    # Index('idxu_application_user_email', 'email', unique=True)
    # Index('idxu_application_user_login_name', 'login_name', unique=True)
    # Index('idx_application_user_last_app_user_id', 'last_app_user_id')
    # Index('idx_application_user_company_id', 'company_id')
    # Index('idx_application_user_is_active', 'is_active')

    # Relationships
    # last_app_user = relationship(
    #     "Application_User",
    #     foreign_keys="Application_User.last_app_user_id"
    # )
    # company = relationship('Company', back_populates='company')
