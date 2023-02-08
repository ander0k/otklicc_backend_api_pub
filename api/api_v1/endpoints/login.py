from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud, models, schemas
from api import deps
from core import security, config
from core.config import settings
from core.security import get_password_hash
from utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token/", response_model=schemas.Token)
def login_access_token(*,
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    app_user = crud.app_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not app_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.app_user.is_active(app_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            subject=app_user.id, code=app_user.code, utype=app_user.utype, email=app_user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token/", response_model=schemas.AppUser)
def test_token(*,
    current_user: models.AppUser = Depends(deps.get_current_user)
) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}/", response_model=schemas.Msg)
def recover_password(*,
    bgtasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    email: str,
) -> Any:
    """
    Password Recovery
    """
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    password_reset_token = generate_password_reset_token(user=app_user)
    send_reset_password_email(bgtasks=bgtasks,
        email_to=app_user.email, email=email, utype=app_user.utype, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(*,
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    elif not crud.app_user.is_active(app_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    passkey = get_password_hash(new_password)
    app_user.passkey = passkey
    db.add(app_user)
    db.commit()
    return {"msg": "Password updated successfully"}

