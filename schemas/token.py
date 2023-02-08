from typing import Optional

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql.base import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: Optional[str] = None
    sub: Optional[str] = None


class TokenBody(BaseModel):
    token: Optional[str] = None

class TokenAuth(BaseModel):
    token: Optional[str] = None
    password: Optional[str] = None

class TokenData(BaseModel):
    id: Optional[str] = None
    utype: Optional[str] = None
    code: Optional[str] = None
    email: Optional[str] = None
    def is_adm(self) -> bool:
        return self.utype == 'ADM'
