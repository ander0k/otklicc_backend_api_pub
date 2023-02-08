from typing import Generator
from utils import decode_token

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import crud, models, schemas
from core import security, config
from core.config import settings
from db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def check_current_user(token: str = Depends(reusable_oauth2)) -> schemas.TokenData:
    try:
        token_data = decode_token(token)
        return schemas.TokenData(**token_data)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = config.EC_TOKEN_EXPIRED, detail = config.ER_TOKEN_EXPIRED)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code = config.EC_BAD_TOKEN, detail = config.ER_BAD_TOKEN)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.AppUser:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = config.EC_TOKEN_EXPIRED, detail = config.ER_TOKEN_EXPIRED)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code = config.EC_BAD_TOKEN, detail = config.ER_BAD_TOKEN)
    user = crud.app_user.get_by_email(db, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    return user


def get_current_active_app_user(
    current_app_user: models.AppUser = Depends(get_current_user),
) -> models.AppUser:
    if not crud.app_user.is_active(current_app_user):
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_NOACTIVE)
    return current_app_user

def get_current_active_superuser(
    current_user: models.AppUser = Depends(get_current_user),
) -> models.AppUser:
    if not crud.app_user.is_superuser(current_user):
        raise HTTPException(
            status_code=config.EC_NOADMIN, detail=config.ER_NOADMIN
        )
    return current_user
