# from datetime import timedelta
from typing import Any
from enum import Enum
#from main import app

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status, BackgroundTasks
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from sqlalchemy.orm import Session

from pydantic import EmailStr
from core import config
import crud,schemas #, models
from os import environ as env
from api import deps
# from core import security
from core.config import settings
from core.security import get_password_hash,verify_password
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth import exceptions
import models
from utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
    send_new_account_email,
)

router = APIRouter()


class AuthType(str, Enum):
    reg = 'reg'
    auth = 'auth'
    gauth = 'gauth'
    restore = 'restore'
    _del = 'del'

class UType(str, Enum):
    CUS = 'CUS'
    HR = 'HR'
    ADM = 'ADM'


@router.get("/docs/")
def get_documentation(*,
    response: Response,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
):
    if current_user.utype != 'ADM':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    response = get_swagger_ui_html(openapi_url=f"{settings.API_V1_STR}/2openapi.json", title="docs")
    return response


@router.get("/auth/", response_model=schemas.auth.Auth)
def auth(*,
         db: Session = Depends(deps.get_db),
         response: Response,
         bgtasks: BackgroundTasks,
         type: AuthType, utype: UType = 'CUS', email: EmailStr, password: str = None
         ) -> Any:
    """
    Начало: регистрации (reg), аутентификации(auth,gauth), восст. пароля(restore), удаление юзера(del)
    """
    if type == 'reg':
        reg_user(response=response, db=db, bgtasks=bgtasks, email=email, password=password, isactive=False, utype=utype)
        return None
    if type == 'auth':
        return auth_user(db=db, email=email, password=password)
    if type == 'gauth':
        return gauth_user(bgtasks=bgtasks, response=response, db=db, password=password, utype=utype)
    if type == 'restore':
        return restore_user(bgtasks=bgtasks, response=response, db=db, email=email)
    if type == 'del':
        return del_user(response=response, db=db, email=email)


@router.delete("/auth/", response_model=schemas.Msg)
def auth(*,
    response: Response,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    fish
    """
    response.status_code = status.HTTP_200_OK
    return {"msg": "OK"}


# обработка ответа от писем щастя (reset password)
@router.put("/auth/", response_model=schemas.Msg)
def final_reset_password(*,
    auth: schemas.TokenAuth,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    финал reset password
    """
    email = verify_password_reset_token(auth.token)
    if not email:
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_BAD_TOKEN)
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    if len(auth.password) < settings.MIN_PSW_LENGTH:
        raise HTTPException(status_code=config.EC_BAD_PARAMS, detail='Короткий пароль')
    passkey = get_password_hash(auth.password)
    app_user.passkey = passkey
    app_user.is_active = True
    try:
        db.add(app_user)
        db.commit()
    finally:
        db.close()
    return {"msg": "Password updated successfully"}
#--------------

# обработка ответа от писем щастя (подтверждение регистрации)
@router.post("/auth/", response_model=schemas.auth.Auth)
def final_reg_user(*,
    tbody: schemas.TokenBody,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    финал регистрации
    """
    email = verify_password_reset_token(tbody.token)
    if not email:
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_BAD_TOKEN)
    app_user = crud.app_user.get_by_email(db=db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    app_user.is_active = True
    r = None
    try:
        db.add(app_user)
        db.commit()
        r = user_to_responce(app_user)
    finally:
        db.close()
    return r
#--------------

#####################################################################

def reg_user(
    response: Response,
    db: Session,
    bgtasks: BackgroundTasks,
    email: str,
    password: str,
    isactive: bool = False,
    utype: str = 'CUS'
) -> Any:
    utype = str.upper(utype)
    if    utype == 'HR': pass
    elif  utype == 'CUS': pass
    else: utype  = 'CUS'

    app_user = crud.app_user.get_by_email(db=db, email=email)
    if app_user:
        if app_user.deleted:      #-- удаленный
            raise HTTPException(status_code=config.EC_DELETED, detail=config.ER_DELETED)
        if app_user.is_active:    #-- активный
            if app_user.passkey:    #-- с паролем
                raise HTTPException(status_code=config.EC_DUPL, detail=config.ER_DUPL)
        else:
            crud.app_user.destroy(db=db, db_obj=app_user)
            app_user = None # не активный
    if password == None or len(password) < settings.MIN_PSW_LENGTH:
        raise HTTPException(status_code=config.EC_BAD_PARAMS, detail='Короткий пароль')
    if app_user:
        user_in = schemas.AppUserUpdate(email=email, password=password, utype=utype)#, is_active=False)
        crud.app_user.update(db=db, db_obj=app_user, obj_in=user_in)
    else:
        user_in = schemas.AppUserCreate(email=email, password=password, utype=utype)
        app_user = crud.app_user.create(db=db, obj_in=user_in, isactive=isactive)
    if not isactive and settings.EMAILS_ENABLED and email:
        token = generate_password_reset_token(app_user)
        send_new_account_email(bgtasks=bgtasks,
            email_to = email, username = email, is_hr=utype == 'HR', token = token
        )
    response.status_code = status.HTTP_201_CREATED
    return app_user


def auth_user(db: Session, email: str, password: str) -> Any:
    # app_user = crud.app_user.authenticate(db=db, email=email, password=password)
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_LOGIN, detail = config.ER_LOGIN)
    if app_user.deleted:
        raise HTTPException(status_code=config.EC_DELETED, detail=config.ER_DELETED)
    if not app_user.passkey:  #-- не зарегистрированный
        if app_user.is_active:
            raise HTTPException(status_code=config.EC_NOPASS, detail=config.ER_NOPASS)
        raise HTTPException(status_code=config.EC_LOGIN, detail = config.ER_LOGIN)
    if not app_user.is_active:
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_NOACTIVE)
    if not verify_password(password, app_user.passkey):
       raise HTTPException(status_code=config.EC_LOGIN, detail = config.ER_LOGIN)
    return user_to_responce(app_user)

# password == token
def gauth_user(bgtasks: BackgroundTasks, response: Response, db: Session, password: str, utype: str) -> Any:
    client_id = env.get('GOOGLE_CLIENT_ID')
    if not client_id:
        try:
            try:
                inf = db.execute(
                    "select value from tcdbinfo where name = 'CLIENT_ID'")
                client_id = inf.first()[0]
            except Exception as err:
                db_error(err)
            env['GOOGLE_CLIENT_ID'] = client_id
        finally:
            db.close()
    try:
        idinfo = id_token.verify_oauth2_token(password, requests.Request(),
                                              client_id)
        email = idinfo['email']
    except (ValueError, exceptions.GoogleAuthError) as err:
        raise HTTPException(status_code=config.EC_EX_AUTH, detail=str(err))
    app_user = crud.app_user.get_by_email(db, email=email)
    # если пользователя с таким email нет в базе - значит надо добавить:
    if not app_user:
        app_user = reg_user(response=response, db=db, bgtasks=bgtasks, email=email, password=password, isactive=True, utype=utype)
    if not crud.app_user.is_active(app_user):
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_NOACTIVE)
    response.status_code = status.HTTP_200_OK
    return user_to_responce(app_user)


def restore_user(bgtasks: BackgroundTasks, response: Response, db: Session, email: str):
    """
    Password Recovery
    """
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    if app_user.deleted:
        raise HTTPException(status_code=config.EC_DELETED, detail=config.ER_DELETED)
    if not app_user.passkey:  #-- не зарегистрированный
        if app_user.is_active:
            raise HTTPException(status_code=config.EC_NOPASS, detail=config.ER_NOPASS)
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    password_reset_token = generate_password_reset_token(app_user)
    send_reset_password_email(bgtasks=bgtasks,
        email_to=app_user.email, email=email, utype=app_user.utype, token=password_reset_token
    )
    response.status_code = status.HTTP_202_ACCEPTED
    return None


def del_user(response: Response, db: Session, email: str) -> Any:
    # cuser = deps.get_current_user()
    # if not crud.app_user.is_superuser(cuser):
    #     raise HTTPException(status_code=config.EC_NOADMIN, detail=config.ER_NOADMIN)
    app_user = crud.app_user.get_by_email(db, email=email)
    if app_user:
        try:
            db.delete(app_user)
            db.commit()
        finally:
            db.close()
    response.status_code = status.HTTP_200_OK
    return None

################################################################################

def db_error(err: BaseException):
    raise HTTPException(status_code=500, detail="Внутренняя ошибка БД")


def user_to_responce(app_user: models.app_user.AppUser) -> Any:
    return {
        'jwt': generate_password_reset_token(app_user)
        ,'code': app_user.code
        , 'img': app_user.img
        , 'utype': app_user.utype
        , 'email': app_user.email
        , 'first_name': app_user.first_name
        , 'last_name': app_user.last_name
    }


def googleinfo_to_responce(db: Session, idinfo) -> Any:
    app_user = crud.app_user.get_by_email(db, email=idinfo['email'])
    if not app_user:
       raise HTTPException(status_code = config.EC_LOGIN, detail = config.ER_LOGIN)
    return {
         'jwt': generate_password_reset_token(app_user)
        , 'code': app_user.code
        , 'img': app_user.img
        , 'utype': app_user.utype
        , 'email': app_user.email
        , 'first_name': app_user.first_name
        , 'last_name': app_user.last_name
    }

