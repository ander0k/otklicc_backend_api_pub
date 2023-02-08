"""
Описание модели валидации геолокации: города, координаты, адреса (geolocation)
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


# Shared properties
class GeolocationBase(BaseModel):
    """
    Геолокация: город, координаты, адрес (geolocation)
    """
    public_id: UUID = Field(
        ...,
        description='публичный (постоянный) уникальный идентификатор записи'
    )
    _record_deleted: Optional[datetime] = Field(
        description='признак и [дата и] время удаления записи, запись '
                    'считается удалённой, если значение этого поля '
                    'отлично от NULL'
    )
    country_a3code: str = Field(
        description='код страны (трехсимвольный alpha-3) по ISO 3166-1',
        max_length=3,
        min_length=3,
        regex='[a-zA-Z]{3}',
        examples='RUS'
    )
    country_name_eng: Optional[str] = Field(
        default=None,
        description='название страны на английском языке в соответствии '
                    'с iso3166'
    )
    country_name_rus: Optional[str] = Field(
        default=None,
        description='название страны на русском языке'
    )
    region_code: Optional[str] = Field(
        default=None,
        description='код региона (для группировки)'
    )
    city_name_eng: Optional[str] = Field(
        default=None,
        description='название города на аглийском языке'
    )
    city_name_rus: Optional[str] = Field(
        default=None,
        description='название города на русском языке'
    )
    latitude: Optional[PositiveFloat] = Field(
        default=None,
        description='географические координаты: широта, значение в градусах '
                    'в виде десятичной дроби'
    )
    longitude: Optional[PositiveFloat] = Field(
        default=None,
        description='географические координаты: долгота, значение в градусах '
                    'в виде десятичной дроби'
    )
    accuracy: Optional[PositiveInt] = Field(
        default=None,
        description='точность указания координат - диаметр окружности в метрах '
                    '(https://www.w3.org/TR//*otklicc.*/geolocation-API/)'
    )
    time_zone_name: Optional[str] = Field(
        default=None,
        description='код (идентификатор) часового пояса в соответствии '
                    'с tz database (Zone name used in value of TZ environment '
                    'variable, https://en.wikipedia.org/wiki/Tz_database)'
    )
    time_zone_utc_offset: Optional[str] = Field(
        default=None,
        description='часовой пояс: смещение относительно UTC (Coordinated '
                    'Universal Time) в часах:минутах в соответсвии с ISO 8601 '
                    '("+03:00" для Москвы)'
    )
    address: Optional[str] = Field(
        default=None,
        description='строка адреса')


# Properties to receive on item creation
class GeolocationCreate(GeolocationBase):
    pass


# Properties to receive on item update
class GeolocationUpdate(GeolocationBase):
    pass


# Properties shared by models stored in DB
class GeolocationInDBBase(GeolocationBase):
    class Config:
        orm_mode = True


# Properties to return to client
class Geolocation(GeolocationInDBBase):
    pass


# Properties stored in DB
class GeolocationInDB(GeolocationInDBBase):
    pass
