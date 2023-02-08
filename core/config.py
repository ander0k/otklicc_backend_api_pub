import secrets
import ssl
from os import environ
from typing import Any, Dict, List, Optional, Union
from starlette import status
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, BaseModel, validator
from pathlib import Path


REG_OK = 'регистрация ок'
AUTH_OK = 'аутентификация ок'
REST_OK = 'восстановление пароля ок'

EC_OK = 200
EC_TOKEN_EXPIRED = 445
ER_TOKEN_EXPIRED = 'токен просрочен не ок'
EC_BAD_TOKEN = 446
ER_BAD_TOKEN = 'токен не расшифрован не ок'
EC_EX_AUTH = status.HTTP_406_NOT_ACCEPTABLE
ER_NOACTIVE = 'пользователь не активен не ок'
EC_NOACTIVE = status.HTTP_423_LOCKED
EC_DELETED = status.HTTP_425_TOO_EARLY
ER_DELETED = 'пользователь удален не ок'
EC_BAD_PARAMS = status.HTTP_400_BAD_REQUEST
ER_BAD_PARAMS = 'некорректные параметры'
ER_DUPL = 'пользователь существует не ок'
ER_COMPANY_DUPL = 'компания уже существует не ок'
EC_DUPL = status.HTTP_409_CONFLICT
EC_NOPASS = status.HTTP_406_NOT_ACCEPTABLE
ER_NOPASS = 'регистрация не завершена не ок'
EC_INACTIVE = status.HTTP_422_UNPROCESSABLE_ENTITY
ER_LOGIN = 'не верный логин пароль не ок'
EC_LOGIN = status.HTTP_401_UNAUTHORIZED
ER_MAIL = 'не верная почта для восстановления не ок'
EC_NOT_FOUND = status.HTTP_404_NOT_FOUND
ER_NOT_FOUND = 'объект не найден'
EC_NOUSER = status.HTTP_404_NOT_FOUND
ER_NOUSER = 'пользователь не существует не ок'
EC_NOPROFILE = status.HTTP_404_NOT_FOUND
ER_NOPROFILE = 'профиль не найден'
ER_NOADMIN = 'не администратор не ок'
EC_NOADMIN = EC_NOUSER
EC_NOACCESS = status.HTTP_403_FORBIDDEN
ER_NOACCESS = 'Недостаточно прав'


class Settings(BaseSettings):
    API_V1_STR: str = "/v1.0"
    SECRET_KEY: str = '' # secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 365
    SERVER_NAME: str = "api.otkli.cc"
    SERVER_HOST: AnyHttpUrl = environ.get('HTTP_HOST', 'http://localhost:8080')
    # URL хоста front-end
    FRONT_HOST: AnyHttpUrl = environ.get('FRONT_HOST', 'http://localhost:8888')
    IMAGES_HOST: str = "https://static.otkli.cc/"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost", "http://localhost:4200", "http://golik.xyz", "https://golik.xyz", 
        "http://localhost:3000", "http://localhost:8080", "http://localhost:8000","https://localhost",
        "https://dev.localhost", "https://api.localhost", "https://db.localhost", "https://localhost:4200", 
        "https://localhost:3000", "https://localhost:8080", "http://dev.otkli.cc", "http://api.otkli.cc",
        "http://db.otkli.cc", "https://stag.otklicc.ab79.info", "https://api.otklicc.ab79.info", 
        "https://db.otklicc.ab79.info", "https://otkli.cc", "http://local.dockertoolbox.tiangolo.com", 
        "http://localhost.tiangolo.com", "https://hr.otkli.cc", "https://adm.otkli.cc", "https://static.otkli.cc",
        "https://164.92.254.193", "https://proxy.otkli.cc"
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "otklicc"
    PROJECT_DIR = Path(__file__).resolve().parent.parent
    SENTRY_DSN: Optional[HttpUrl] = ""
    MIN_PSW_LENGTH = 6

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if not v or len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str = "db.otkli.cc"
    # POSTGRES_USER: str = "api.otkli.cc"
    # POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "db_otklicc"
    SQLALCHEMY_DATABASE_URI: str = environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:sa@localhost:6432/db_otklicc?application_name=api.otkli.cc app')

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            # return values["PROJECT_NAME"]
            return "otklicc"
        return v

    EMAIL_TOKEN_EXPIRE_HOURS: int = 24
    EMAIL_TEMPLATES_DIR = PROJECT_DIR.joinpath("email-templates/build")
    EMAILS_ENABLED: bool = True

    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "ander@ab79.info"
    FIRST_SUPERUSER_PASSWORD: str = "zzz"
    USERS_OPEN_REGISTRATION: bool = False
    CRON_MAIL_PERIOD = 1*60 # seconds
    CRON_MAIL_ON = True
    CRON_DEDLINE_ON = True
    CRON_DEDLINE_HOUR='09'
    CRON_GARBAGE_HOUR = '07'
    CRON_GARBAGE_ON = True


class TcDbInfo(BaseModel):
    name: Optional[str]
    mask: Optional[str]
    value: Optional[str]
    tag: Optional[int]


# class Config:
#     case_sensitive = True


settings = Settings()
