import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from db.base_class import Base
from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship

PUBLIC_ID_SERVER_DEFAULT_TEXT = sqlalchemy.sql.expression.text(
    "encode(digest(CAST(gen_random_uuid() as TEXT), 'sha256'), 'hex')"
)


class Geolocation(Base):
    """Datamodel for geolocation
    модель таблицы геолокации: города, координаты, адреса
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
        server_default=sqlalchemy.sql.expression.text('current_timestamp'),
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
    country_a3code = Column(
        postgres_dialect.TEXT,
        nullable=False,
        comment='код страны (трехсимвольный alpha-3) по ISO 3166-1'
    )
    country_name_eng = Column(
        postgres_dialect.TEXT,
        comment='название страны на английском языке в соответствии с iso3166'
    )
    country_name_rus = Column(
        postgres_dialect.TEXT,
        comment='название страны на русском языке'
    )
    region_code = Column(
        postgres_dialect.TEXT,
        comment='код региона (для группировки)'
    )
    city_name_eng = Column(
        postgres_dialect.TEXT,
        comment='название города на аглийском языке'
    )
    city_name_rus = Column(
        postgres_dialect.TEXT,
        comment='название города на русском языке'
    )
    latitude = Column(
        postgres_dialect.FLOAT,
        comment='географические координаты: широта, значение в градусах '
                'в виде десятичной дроби'
    )
    longitude = Column(
        postgres_dialect.FLOAT,
        comment='географические координаты: долгота, значение в градусах '
                'в виде десятичной дроби'
    )
    accuracy = Column(
        postgres_dialect.INTEGER,
        comment='точность указания координат - диаметр окружности в метрах '
                '(https://www.w3.org/TR//*otklicc.*/geolocation-API/)'
    )
    time_zone_name = Column(
        postgres_dialect.TEXT,
        comment='код (идентификатор) часового пояса в соответствии '
                'с tz database (Zone name used in value of TZ environment '
                'variable, https://en.wikipedia.org/wiki/Tz_database)'
    )
    time_zone_utc_offset = Column(
        postgres_dialect.TEXT,
        comment='часовой пояс: смещение относительно UTC (Coordinated '
                'Universal Time) в часах:минутах в соответсвии с ISO 8601 '
                '("+03:00" для Москвы)'
    )
    address = Column(
        postgres_dialect.TEXT,
        comment='строка адреса')

    # Constraints
    # объявление уникального ключа на public_id сделано через Constraint, чтобы
    # иметь возможность задать возможность отложенной проверки (deferrable=True)
    # UniqueConstraint(
    #     ['public_id'], name='idxu_geolocation_public_id', deferrable=True
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
