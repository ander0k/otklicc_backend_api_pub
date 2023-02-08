from typing import Any,List
from core import config
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from api import deps
import crud
from schemas import TokenData, ResultPut, ResultDel
from utils import send_interview_email

router = APIRouter()


@router.get("/", response_model = dict)
def get_result(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    page_rows   : int = 5,
    page        : int = 1,
    code        : str,
) -> dict:
    if current_user.utype != 'HR':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    vacancy = crud.vacancy.get_by_code(db=db, code=code)
    if not vacancy:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
    vac_info = crud.vacancy.get_hrdata(db=db, vac_id=vacancy.id, inc_counter=False)
    if not (current_user.email in vac_info.vac_owner_list or current_user.email in vac_info.vac_viewer_list):
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    dct = {}
    lst = []
    if vac_info.vac_owner_list:
        lst = list(vac_info.vac_owner_list.keys())  # ','.join(lst)
    dct['vac_owner_list'] = lst
    lst = []
    if vac_info.vac_viewer_list:
        lst = list(vac_info.vac_viewer_list.keys())
    dct['vac_viewer_list'] = lst
    lst = crud.result.get(
        db        = db,
        page_rows = page_rows,
        page      = page,
        vac_id    = vacancy.id,
    )
    dct['max_grade_summ'] = lst.pop()
    dct['scored_list'] = lst
    return dct


@router.put("/", response_model = None)
def put_result(*,
    db: Session = Depends(deps.get_db),
    bgtasks: BackgroundTasks,
    current_user: TokenData = Depends(deps.check_current_user),
    result: ResultPut
) -> None:
    try:
        if current_user.utype != 'HR':
            raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
        vacancy = crud.vacancy.get_by_code(db=db, code=result.code)
        if not vacancy:
            raise HTTPException(status_code=config.EC_NOT_FOUND, detail='vacancy not found')
        vac_info = crud.vacancy.get_hrdata(db=db, vac_id=vacancy.id, inc_counter=False)
        if not current_user.email in vac_info.vac_owner_list and not current_user.email in vac_info.vac_viewer_list:
            raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
        user = crud.app_user.get_by_code(db=db, code=result.profile_code)
        if not user:
            raise HTTPException(status_code=config.EC_NOT_FOUND, detail='profile not found')
        hr = crud.app_user.get_by_id(db=db, id=current_user.id)
        company = crud.company.get(db=db, id=vacancy.company_id)
        if not company:
            raise HTTPException(status_code=config.EC_NOT_FOUND, detail='company not found')
    finally:
        db.close()
    send_interview_email(
        bgtasks=bgtasks,
        email_to=user.email,
        vac_code=result.code,
        vacancy_title=vacancy.title,
        company_code=company.code,
        company_name=company.name,
        hr_name=hr.first_name,
        hr_last_name=hr.last_name,
        hr_email=hr.email,
        content=result.content
    )


@router.delete("/", response_model = None)
def delete_result(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    result: ResultDel,
) -> dict:
    if current_user.utype != 'HR':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    vacancy = crud.vacancy.get_by_code(db=db, code=result.code)
    if not vacancy:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail='vacancy not found')
    vac_info = crud.vacancy.get_hrdata(db=db, vac_id=vacancy.id, inc_counter=False)
    if not current_user.email in vac_info.vac_owner_list and not current_user.email in vac_info.vac_viewer_list:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)

    return crud.result.delete(db=db, vac_id=vacancy.id, cus_code=result.profile_code)



