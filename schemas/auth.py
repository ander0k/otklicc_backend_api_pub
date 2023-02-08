from typing import Optional

from pydantic import BaseModel, EmailStr, AnyUrl
from uuid import UUID


# Shared properties
class AuthBase(BaseModel):
    # регистрация ок | аутентификация ок | восстановление пароля ок | пользователь существует не ок | неверный логин пароль не ок | неверная почта для восстановления не ок
    jwt: Optional[str]
    code: Optional[str]
    img: Optional[AnyUrl]
    utype: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

# Additional properties to return via API
class Auth(AuthBase):
    pass
