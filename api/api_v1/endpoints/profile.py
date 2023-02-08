from typing import Any,Optional
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from core import config
import crud,json
import schemas
from os import environ as env
from api import deps
from utils import obj2json, verify_password_reset_token
from schemas.profile import ProfileDel,ProfilePut
from schemas.app_user import AppUserUpdate

router = APIRouter()


PF_HIDDEN = 10  # скрыть от всех
PF_OTKLIC = 20  # видно только после отклика
PF_PUBLIC = 30  # видно всем


@router.get("/list/")
def profile_list(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    skip: int = 0,
    limit: int = 100,
) -> dict:
    """
    Реестр профилей
    """
    if current_user.utype != 'ADM':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.profile.get_multi(db=db, skip=skip,limit=limit)


@router.get("/{code}/", response_model=dict)
def get_prof(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    code: str = ''
) -> Any:
    """
    Для неавторизованных: Прочитать public профиль по коду
    """
    app_user = crud.app_user.get_by_code(db, code=code)
    if not app_user or not app_user.is_active or app_user.prof_view != PF_PUBLIC or app_user.is_adm():
        raise HTTPException(status_code=config.EC_NOPROFILE,
                            detail=config.ER_NOPROFILE)
    return crud.profile.get(db, app_user=app_user)


@router.get("/", response_model=dict)
def get_profile(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    code: str = None
) -> Any:
    if code != None:
        matrix = ["CUSHR","HRCUS","HRHR"]
        app_user = crud.app_user.get_by_code(db, code=code)
        if not app_user or not app_user.is_active:
            raise HTTPException(status_code=config.EC_NOPROFILE, detail=config.ER_NOPROFILE)
        forself = current_user.id == app_user.id
        if not forself and not current_user.is_adm():  # если не о себе
            if app_user.prof_view == PF_HIDDEN or app_user.is_adm():  #  скрыть от всех, ADM скрыт всегда
                raise HTTPException(status_code=config.EC_NOPROFILE, detail=config.ER_NOPROFILE)
            elif app_user.prof_view == PF_OTKLIC:
                if  not( (current_user.utype + app_user.utype) in matrix ) or \
                    not crud.profile.HasReply(db=db, current_user=current_user, app_user=app_user):
                    raise HTTPException(
                        status_code=config.EC_NOPROFILE, detail=config.ER_NOPROFILE)
            elif app_user.prof_view == PF_PUBLIC:
                pass
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='invalid prof_view')
    else:
        app_user = crud.app_user.get_by_id(db, id=current_user.id)
    return crud.profile.get(db, app_user=app_user, current_user=current_user)


def merge_dict(old: str, new: dict) -> str:
    if not old: 
        if not new: return None
        return obj2json(new)
    if not new: return old
    result = json.loads(old)
    for k,v in new.items():
        result[k] = v
    return obj2json(result)


@router.put("/")
def put_profile(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(
        deps.check_current_user),
    profile: ProfilePut
) -> Any:
    app_user = crud.app_user.get_by_id(db, id=current_user.id)
    user_update = AppUserUpdate(**profile.__dict__)
    for k, v in profile:  # update пытается писать в базу все поля user_update, поэтому None-поля вычеркиваем
        if v == None:
            user_update.__dict__.pop(k, None)

    if profile.education:
        user_update.educations = merge_dict(app_user.educations, profile.education)
    if profile.job:
        user_update.jobs = merge_dict(app_user.jobs, profile.job)
    crud.app_user.update(db, db_obj=app_user, obj_in=user_update)
    return {}


@router.put("/approve/")
def put_profile_approve(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    tbody: schemas.TokenBody,
) -> Any:
    """
    закрепить временно добавленного пользователя
    """
    email = verify_password_reset_token(tbody.token)
    if not email:
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_BAD_TOKEN)
    app_user = crud.app_user.get_by_email(db=db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    if app_user.is_active:
        return {}
    app_user.is_active = True
    try:
        db.add(app_user)
        db.commit()
    finally:
        db.close()
    return {}



class Notif(BaseModel):
    token: Optional[str] = None
    notifications: Optional[str] = None

@router.put("/notifications/")
def put_profile_notif(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    notif: Notif 
) -> None:
    email = verify_password_reset_token(notif.token)
    if not email:
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_BAD_TOKEN)
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    notifications = app_user.notifications if app_user.notifications else 10
    if notifications == 40: return
    notifications = 40 if notif.notifications == 'off' else notifications + 10
    crud.app_user.update(db, db_obj=app_user, obj_in={'notifications': notifications})



# @router.delete("/{code}/")
def del_profile(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(
        deps.check_current_user),
    code: str,
    prof_del: ProfileDel
) -> Any:
    """
    Только для отладки для ADM! Удалить из профиля по коду.
    """
    if not current_user.is_adm(): code = None
    if code:
        app_user = crud.app_user.get_by_code(db, code=code)
    else:
        app_user = crud.app_user.get_by_id(db, id=current_user.id)
    if prof_del.delete_acc:
        crud.app_user.remove(db=db, db_obj=app_user)
        return {}
    if app_user.utype != 'CUS':
        prof_del.skills = None
    if app_user.utype != 'HR':
        prof_del.comp_viewer_list = None
        prof_del.vac_owner_list = None
        prof_del.vac_viewer_list = None
    crud.profile.remove(db=db, app_user=app_user, data_obj=prof_del)
    return {}


@router.delete("/")
def delete_profile(*,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(
        deps.check_current_user),
    prof_del: ProfileDel
) -> Any:
    return del_profile(request=request, db=db, current_user=current_user, code=None, prof_del=prof_del)


