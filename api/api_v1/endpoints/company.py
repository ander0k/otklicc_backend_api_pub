from crud import crud_app_user, crud_company
from typing import Any,List
from copy import copy

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError

from core import config
import crud
import schemas
import models
from models import Company
from api import deps
from utils import send_comp_emails,generate_password_reset_token
from schemas.company import CompanyRd, CompanyDel, CompanyPost, CompanyPut, \
                            STATUS_DRAFT, STATUS_MODER, STATUS_REJECT, STATUS_PUBLIC, STATUS_ARCHIVE

router = APIRouter()


@router.get("/list/")#, response_model=List[dict])
def company_list(*,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    skip: int = 0,
    limit: int = 100,
) -> dict:
    """
    Реестр компаний
    """
    if current_user.utype != 'ADM':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.company.get_multi(db=db, skip=skip,limit=limit)


@router.get("/{code}/", response_model=dict)
def get_comp_anonimous(*,
    db: Session = Depends(deps.get_db),
    code: str = None
) -> dict:
    """
    Чтение неавторизованным пользователем
    """
    return get_company(db=db, current_user=None, code=code)


@router.get("/", response_model=dict)
def get_company(*,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    code: str = None
) -> dict:
    """
    Чтение данных компании
    """
    comp = crud.company.get_by_code(db=db, code=code)
    if not comp:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
    utype = 'CUS'
    if current_user: utype = current_user.utype
    if comp.status < STATUS_PUBLIC:
        if utype == 'CUS':
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    # owner_email, comp_viewer_list: пары {email:fio}
    vwrlist = crud.company.get_vwrlist(db=db, company_id=comp.id)
    # всякое секретное могут смотреть только ADM, HR сладельцы HR из списка comp_viewer_list
    can = utype == 'ADM' \
                or current_user and( \
                   utype != 'CUS' and current_user.id == comp.owner_user_id \
                or vwrlist and current_user.email in vwrlist)
    if comp.status < STATUS_PUBLIC and not can:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    company = CompanyRd(**comp.__dict__).__dict__
    if can:
        company['comp_viewer_list'] = vwrlist
    else:
        company.pop('owner_email', None)
        company.pop('owner_name', None)
    return company


def send_emails(
    db: Session,
    bgtasks: BackgroundTasks,
    emails_to: str,
    company: Company, 
    asowner: bool,
    old_own: dict,
    new_own: dict,
) -> None:
    tokens = {}
    if emails_to:
        users = crud_app_user.app_user.get_by_emails(db=db, emails=emails_to.split(','))
        for email, user in users.items():
            tokens[email] = generate_password_reset_token(user)
    bgtasks.add_task(send_comp_emails,
    # send_comp_emails(
        emails_to=emails_to,
        tokens=tokens,
        company_name=company.name,
        company_code=company.code,
        asowner=asowner,
        old_own=old_own,
        new_own=new_own,
    )


@router.post("/", response_model=dict)
def create_company(*,
    db: Session = Depends(deps.get_db),
    bgtasks: BackgroundTasks,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    company: CompanyPost
) -> dict:
    """
    Создание компании
    """
    if current_user.utype != 'HR':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    if company.status > STATUS_MODER:
        raise HTTPException(status_code=config.EC_BAD_PARAMS, detail=config.ER_BAD_PARAMS)
    dct = copy(company.__dict__) # данные
    for k, v in company:  # update пытается писать в базу все поля, поэтому None-поля вычеркиваем
        if v == None: dct.pop(k, None)
    if company.color: 
        try:    tmp = int(company.color, 16)
        except: dct.pop('color',  None)
    if company.sec_color:
        try:    tmp = int(company.sec_color, 16)
        except: dct.pop('sec_color', None)
    dct.pop('comp_viewer_list', None) # это не поле в app_user
    dct.pop('owner_email', None)      # это не поле в app_user
    dct['owner_user_id'] = current_user.id
    try:
        db_obj = crud.company.create(db=db, company=Company(**dct))
    except DBAPIError as err:
        code = config.EC_DUPL if err.orig.__class__.__name__ == 'UniqueViolation' else status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(status_code = code, detail =config.ER_COMPANY_DUPL if code == config.EC_DUPL else str(err))
    if company.comp_viewer_list:
        mails = crud.company.make_viewers(db=db, company=db_obj, comp_viewer_list=company.comp_viewer_list)
        if mails:
            send_emails(
                db=db,
                bgtasks=bgtasks,
                emails_to=mails,
                company=db_obj,
                asowner=False,
                old_own=None,
                new_own=None,
            )
    return {"name": db_obj.name, "code": db_obj.code}


@router.put("/", response_model=dict)
async def put_company(*,
    db: Session = Depends(deps.get_db),
    bgtasks: BackgroundTasks,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    company: CompanyPut
) -> dict:
    """
    Редактирование компании
    """
    if current_user.utype == 'CUS':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    # проверка значений status
    if company.status:
        if current_user.utype == 'HR' and company.status != STATUS_ARCHIVE and company.status != STATUS_MODER \
            or current_user.is_adm() and company.status != STATUS_PUBLIC and  company.status != STATUS_REJECT:
            raise HTTPException(status_code=config.EC_BAD_PARAMS, detail=config.ER_BAD_PARAMS)
    db_obj = crud.company.get_by_code(db=db, code=company.code)
    if not db_obj:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
    if not current_user.is_adm() and current_user.id != db_obj.owner_user_id:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    dct = copy(company.__dict__) # данные для замены
    for k, v in company:  # update пытается писать в базу все поля, поэтому None-поля вычеркиваем
        if v == None: dct.pop(k, None)
    if company.color: 
        try:    tmp = int(company.color, 16)
        except: dct.pop('color',  None)
    if company.sec_color:
        try:    tmp = int(company.sec_color, 16)
        except: dct.pop('sec_color', None)
    dct.pop('comp_viewer_list', None)
    if not current_user.is_adm() and dct.get('verified', None):
        raise HTTPException(status_code=config.EC_NOADMIN, detail=config.ER_NOADMIN)
    old_own_id = db_obj.owner_user_id
    if current_user.utype == 'HR':
        major = company.name and company.name != db_obj.name
        if not major and company.status == 20 and db_obj.status == 40:
                dct.pop('status')
        if major and company.status != 50 and db_obj.status != 50:
                dct['status'] = 20
    db_obj = crud.company.update(db=db, db_obj=db_obj, update_data=dct)
    new_own_id = db_obj.owner_user_id
    old_own = {}
    new_own = {}
    if new_own_id != old_own_id: # власть меняется
        if old_own_id:
            user = crud.app_user.get(db=db, id=old_own_id)
            old_own["email"] = user.email
            old_own["token"] = generate_password_reset_token(user)
        if new_own_id:
            user = crud.app_user.get(db=db, id=new_own_id)
            new_own["email"] = user.email
            new_own["token"] = generate_password_reset_token(user)
    mails = None
    if company.comp_viewer_list:
        mails = crud.company.make_viewers(db=db, company=db_obj, comp_viewer_list=company.comp_viewer_list)
    if mails or old_own or new_own:
        send_emails(
            db=db,
            bgtasks=bgtasks,
            emails_to=mails,
            company=db_obj,
            asowner=False,
            old_own=old_own,
            new_own=new_own,
        )
    return {"name": db_obj.name, "code": db_obj.code}


@router.delete("/", response_model=dict)
def del_comp_viewers(*,
    db: Session = Depends(deps.get_db),
    company_in: CompanyDel,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
) -> dict:
    """
    Удаление из перечня viewer_list
    """
    company = crud.company.get_by_code(db=db,code=company_in.code)
    if not company:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
    if current_user.utype != 'ADM' and company.owner_user_id != current_user.id:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    crud.company.del_viewers(db=db, company_id=company.id, viewer_list=company_in.comp_viewer_list)
    return {}