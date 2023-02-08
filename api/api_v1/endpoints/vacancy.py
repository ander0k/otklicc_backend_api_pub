from crud import crud_app_user,crud_cron
from schemas.vacancy import CompanyCard,VacancyCard,VacancyPost,\
                            VacancyAnyPut,VacancyPut,VacancyDel,\
     STATUS_DRAFT, STATUS_MODER, STATUS_REJECT, STATUS_PUBLIC, STATUS_ARCHIVE

from uuid import UUID
from typing import Any, List
from core import config
from copy import copy

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

import asyncio
import crud, models, schemas
from schemas.vacancy import VacancyBase
from schemas.company import Company

from utils import  \
    send_confirm_responce_email,\
    send_vacancy_add_list_email,\
    send_vac_archive_mail,\
    generate_password_reset_token,\
    verify_password_reset_token,\
    list2csv
from api import deps

router = APIRouter()

CUS_ST_RECOMEND  = 10
CUS_ST_SHOWED    = 20
CUS_ST_BOOKMRK   = 30
CUS_ST_RESPONSED = 40
CUS_ST_SCORED    = 50


@router.get("/list/")
def vac_list(*,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    skip: int = 0,
    limit: int = 100,
) -> dict:
    """
    Реестр вакансий
    """
    if current_user.utype != 'ADM':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.vacancy.get_multi(db=db, skip=skip,limit=limit)


@router.get("/{code}/", response_model=dict)
def vacancy_get_anon(*,
    db: Session = Depends(deps.get_db),
    code: str = None
) -> Any:
    """
    Получить вакансию без авторизации
    """
    return vacancy_get(db=db, current_user=None, code=code)


@router.get("/", response_model=dict)
def vacancy_get(*,
        db: Session = Depends(deps.get_db),
        current_user: schemas.TokenData = Depends(deps.check_current_user),
        code: str = None
) -> Any:
    """
    Получить вакансию (авторизованный пользователь)
    """
    utype = 'CUS'
    if current_user: utype = current_user.utype
    vacancy = copy(crud.vacancy.get_by_code(db=db, code=code))
    if not vacancy:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
    if vacancy.status < STATUS_PUBLIC:
        if utype == 'CUS':
            raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
    company = copy(crud.company.get(db=db, id=vacancy.company_id))
    if not company:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail='company not found')
    vac_info = crud.vacancy.get_hrdata(db=db, vac_id=vacancy.id, inc_counter=utype == 'CUS')
    # всякое секретное могут смотреть только ADM, HR сладельцы HR из списка comp_viewer_list
    can = utype == 'ADM'
    if not can and utype != 'CUS':
        can = vac_info.vac_owner_list  and current_user.email in vac_info.vac_owner_list or\
              vac_info.vac_viewer_list and current_user.email in vac_info.vac_viewer_list
    if not can and vacancy.status != STATUS_PUBLIC and vacancy.status != STATUS_ARCHIVE:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)

    compcard = CompanyCard()
    for k,v in compcard:
        v = company.__dict__.get(k, None)
        if v: compcard.__dict__[k] = v
    vacard = VacancyCard()
    for k,v in vacard:
        v = vacancy.__dict__.get(k, None)
        if v != None: vacard.__dict__[k] = v
    vacard.view_count = vac_info.view_count
    dct = {
        "company_card": compcard,
        "vacancy_card": vacard
    }
    dct["professions"] = vacancy.professions.split(',') if vacancy.professions else []
    dct["geos"] = vacancy.geos.split(',') if vacancy.geos else []
    utype = current_user.utype if current_user else 'ANO'
    cus_id = current_user.id if utype == 'CUS' else None
    cus_status, dct['terms'], dct['demands'], responses, metatags, coefficients, dct['applies'] =\
        crud.vacancy.get_data(db=db, vac_id=vacancy.id, candidate_id=cus_id)
    if utype == 'CUS':
        dct['responses'] = responses
        dct['cus_status'] = cus_status

    if utype != 'ANO':
        if utype == 'ADM':
            dct['metatags'] = metatags
            dct['coefficients'] = coefficients
        if utype == 'ADM' or vac_info.vac_owner_list and current_user.email in vac_info.vac_owner_list\
                          or vac_info.vac_viewer_list and current_user.email in vac_info.vac_viewer_list:
            dct['vac_owner_list'] = vac_info.vac_owner_list
            dct['vac_viewer_list'] = vac_info.vac_viewer_list
    return dct


def send_emails(
    vacancy_name: str,
    vacancy_code: str,
    vac_owner_list: str,
    vac_viewer_list: str,
    tokens: dict, # пара email-token; элементов может быть больше, чем в emails_to
)-> None:
    if vac_viewer_list:
        send_vacancy_add_list_email(
            emails_to=vac_viewer_list,
            tokens=tokens,
            vacancy_name=vacancy_name,
            vacancy_code=vacancy_code,
            asowner=False
        )
    if vac_owner_list:
        send_vacancy_add_list_email(
            emails_to=vac_owner_list,
            tokens=tokens,
            vacancy_name=vacancy_name,
            vacancy_code=vacancy_code,
            asowner=True
        )


def check_send_emails(
        db: Session,
        bgtasks: BackgroundTasks,
        vacancy_name: str,
        vacancy_code: str,
        vac_owner_list: str,
        vac_viewer_list: str,
)-> None:
    if not vac_viewer_list and not vac_owner_list: return
    tokens = {} #  - пары email-token
    # получить в tokens уникальный перечень email, общий для viewer_list и owner_list
    if vac_viewer_list:
        for email in vac_viewer_list.split(','):
            if not tokens.get(email):
                tokens[email] = ''
    if vac_owner_list:
        for email in vac_owner_list.split(','):
            if not tokens.get(email):
                tokens[email] = ''
    # получить в users всех пользователей, кому слать письма
    users = crud.app_user.get_by_emails(db=db, emails=tokens.keys())
    # заполнить tokens
    for email in tokens.keys():
        tokens[email] = generate_password_reset_token(users[email])
    if tokens:
        bgtasks.add_task(send_emails,
            vacancy_name=vacancy_name,
            vacancy_code=vacancy_code,
            vac_owner_list=vac_owner_list,
            vac_viewer_list=vac_viewer_list,
            tokens=tokens,
        )


@router.post("/", response_model=dict)
def vacancy_new(*,
    db: Session = Depends(deps.get_db),
    bgtasks: BackgroundTasks,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    vac_post: VacancyPost = None
) -> Any:
    """
    Создание вакансии
    """
    if current_user.utype != 'HR':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    if not vac_post.vacancy_card.title or not vac_post.professions or not vac_post.geos\
           or not vac_post.vacancy_card.status or not vac_post.vacancy_card.busyness \
           or not vac_post.vacancy_card.currency or not vac_post.vacancy_card.term:
        raise HTTPException(status_code=config.EC_BAD_PARAMS, detail='title,status,profession,geo,currency,term is required')
    company = crud.company.get_by_code(db=db, code=vac_post.comp_code)
    if not company:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail='Company not found')
    comp_vwrlist = crud.company.get_vwrlist(db=db, company_id=company.id)
    if current_user.email != company.owner_email and not current_user.email in comp_vwrlist:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    if vac_post.vac_owner_list:
        if current_user.email not in vac_post.vac_owner_list:
            vac_post.vac_owner_list.append(current_user.email)
    else:
        vac_post.vac_owner_list = [current_user.email]
    info = crud.vacancy.create(db=db, obj_in=vac_post, company_id=company.id)
    check_send_emails(
        db=db,
        bgtasks=bgtasks,
        vacancy_name=info.title,
        vacancy_code=info.code,
        vac_owner_list=info.vac_owner_list,
        vac_viewer_list=info.vac_viewer_list,
    )
    return {"title": info.title, "code": info.code}


@router.put("/{code}/", response_model=dict)
def vacancy_responce_anonimous(*,
    db: Session = Depends(deps.get_db),
    bgtasks: BackgroundTasks,
    code: str,
    vacancy_in: VacancyAnyPut,
) -> Any:
    '''
    Отклик неавторизованного
    '''
    vacancy_in.email = vacancy_in.email.lower()
    vac = crud.vacancy.get_by_code(db=db, code=code)
    if not vac:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    if vac.status != STATUS_PUBLIC:
        raise HTTPException(status_code=config.EC_NOACTIVE, detail="Vacancy is not active")
    app_user = crud.app_user.get_by_email(db=db, email=vacancy_in.email)
    if not app_user:
        user_in = schemas.AppUserCreate(email=vacancy_in.email, password='', utype='CUS')
        app_user = crud.app_user.create(db=db, obj_in=user_in, isactive=False)
    token = generate_password_reset_token(app_user)
    crud.vacancy.new_responses(db=db, user_id=app_user.id, draft=True, responses=vacancy_in.responses, metatags=None)
    send_confirm_responce_email(bgtasks=bgtasks,
        email_to=app_user.email, username=app_user.email, vac=vac, token=token
    )
    return {}


# обработка ответа от писем щастя (подтверждение отклика)
@router.post("/otk/", response_model=schemas.auth.Auth)
def vac_reply_confirm(*,
    tbody: schemas.TokenBody,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    подтверждение отклика от анонима
    """
    email = verify_password_reset_token(tbody.token)
    if not email:
        raise HTTPException(status_code=config.EC_NOACTIVE, detail=config.ER_BAD_TOKEN)
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        raise HTTPException(status_code=config.EC_NOUSER, detail=config.ER_NOUSER)
    crud.vacancy.otk_enable(db=db, user_id=app_user.id)
    return {}


@router.put("/", response_model=dict)
def vacancy_modify(*,
        db: Session = Depends(deps.get_db),
        bgtasks: BackgroundTasks,
        current_user: schemas.TokenData = Depends(deps.check_current_user),
        vacancy_in: VacancyPut,
) -> Any:
    """
    Изменение вакансии.
    """
    vac = crud.vacancy.get_by_code(db=db, code=vacancy_in.code)
    if not vac:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail='vacancy not found')
    if current_user.utype == 'CUS':
        if vac.status != STATUS_PUBLIC:
            raise HTTPException(status_code=config.EC_NOACTIVE, detail="Vacancy is not active")
        put_obj = VacancyPut()
        put_obj.responses = vacancy_in.responses
        if vacancy_in.bookmarked != None:
            put_obj.bookmarked = vacancy_in.bookmarked
        crud.vacancy.update(db=db, user_id=current_user.id, vac_id=vac.id, put_obj=put_obj)
    else:   # ADM & HR
        vacancy_in.bookmarked = None
        vacancy_in.responses = None
        if current_user.utype == 'HR':
            vacancy_in.metatags = None
            if vacancy_in.vacancy_card and vacancy_in.vacancy_card.status:
                if vacancy_in.vacancy_card.status != STATUS_MODER and vacancy_in.vacancy_card.status != STATUS_ARCHIVE: 
                    raise HTTPException(status_code=config.EC_BAD_PARAMS, detail='bad status')
            #  Проверить наличие тек. п-ля в перечне владельцев вакансии
            vac_info = crud.vacancy.get_hrdata(db=db,vac_id=vac.id)
            if not current_user.email in vac_info.vac_owner_list:
                raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
            vacancy_in.coefficients = None
            vacancy_in.metatags = None
            has_major = vacancy_in.vacancy_card and \
                (vacancy_in.vacancy_card.title and vacancy_in.vacancy_card.title != vac.title or \
                 vacancy_in.vacancy_card.about and vacancy_in.vacancy_card.about != vac.about or \
                 vacancy_in.vacancy_card.leave_days and vacancy_in.vacancy_card.leave_days != vac.leave_days
                ) or \
                vacancy_in.professions and list2csv(vacancy_in.professions) != vac.professions or \
                vacancy_in.geos and list2csv(vacancy_in.geos) != vac.geos
            if not has_major and (vacancy_in.demands or vacancy_in.terms):
                cus_status, terms, demands, responses, metatags, coefficients, applies =\
                    crud.vacancy.get_data(db=db, vac_id=vac.id, candidate_id=None)
                has_major = vacancy_in.demands and vacancy_in.demands != demands or \
                            vacancy_in.terms and vacancy_in.terms != terms
            if vacancy_in.vacancy_card and vacancy_in.vacancy_card.status == STATUS_ARCHIVE:
                has_major = None
            if has_major:
                if not vacancy_in.vacancy_card: vacancy_in.vacancy_card = VacancyBase(status=STATUS_MODER)
                vacancy_in.vacancy_card.status = STATUS_MODER
            else:
                if vacancy_in.vacancy_card and vacancy_in.vacancy_card.status == STATUS_MODER and vac.status == STATUS_PUBLIC:
                    vacancy_in.vacancy_card.status = None
        else:   # ADM
            if vacancy_in.vacancy_card and vacancy_in.vacancy_card.status:
                if vacancy_in.vacancy_card.status != STATUS_REJECT and vacancy_in.vacancy_card.status != STATUS_PUBLIC:
                    raise HTTPException(status_code=config.EC_BAD_PARAMS, detail='bad status')
                if vacancy_in.vacancy_card.status == STATUS_PUBLIC:
                    vacancy_in.vacancy_card.status = -STATUS_PUBLIC  # триггер должен сработать даже если вакансия уже опубликована (40)
        info = crud.vacancy.update(db=db, user_id=current_user.id, vac_id=vac.id, put_obj=vacancy_in)
        if vac.status == STATUS_PUBLIC and vacancy_in.vacancy_card and vacancy_in.vacancy_card.status == STATUS_ARCHIVE:
            # asyncio.run(crud.crud_cron.cron_dedline(force=True))
            bgtasks.add_task(crud.crud_cron.cron_dedline, force=True)
        else:
            check_send_emails(
                db=db,
                bgtasks=bgtasks,
                vacancy_name=vac.title,
                vacancy_code=vac.code,
                vac_owner_list=info.vac_owner_list,
                vac_viewer_list=info.vac_viewer_list,
            )
        return {}



@router.delete("/", response_model=dict)
def vacancy_delete(*,
        db: Session = Depends(deps.get_db),
        current_user: schemas.TokenData = Depends(deps.check_current_user),
        vacancy_in: VacancyDel
) -> Any:
    """
    Удаление вакансии.
    """
    vacancy = crud.vacancy.get_by_code(db=db, code=vacancy_in.code)
    if not vacancy:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail='vacancy not found')
    if current_user.utype == 'CUS':
        # отсекаем лишнее
        vacancy_in = VacancyDel(responses=vacancy_in.responses)
    else:
        vacancy_in.responses = None
        # эти удаления может или админ, или владелец вакансии
        can = current_user.is_adm()
        if not can: # Проверить наличие тек. п-ля в перечне владельцев вакансии
            vac_info = crud.vacancy.get_hrdata(db=db,vac_id=vacancy.id)
            can = current_user.email in vac_info.vac_owner_list
        if not can:
            raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    crud.vacancy.remove(db=db, vac_id=vacancy.id, cus_id=current_user.id, vacancy=vacancy_in)
    return {}


@router.get("/scoring/{demand_id}/", response_model=List[schemas.VcnResponse])
def read_scoring(*,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    demand_id: UUID,
    current_user: models.AppUser = Depends(
        deps.get_current_active_app_user
),
) -> Any:
    """
    Получить список откликов на заданное (otklicc.vcn_response.demand_id) требование вакансии.
    """
    vcn_responses = crud.crud_vcn_response.vcn_response.get_list_by_demand(
        db, skip=skip,
        limit=limit,
        demand_id=demand_id
    )

    return vcn_responses


@router.put("/scoring/{demand_id}/", response_model=schemas.VcnResponse)
def update_vcn_response(*,
    db: Session = Depends(deps.get_db),
    demand_id: UUID,
    response_id: UUID,
    response_in: schemas.VcnResponseUpdate,
    current_user: models.AppUser = Depends(deps.get_current_active_app_user),
) -> Any:
    """
    Изменение отклика.
    """
    vcn_response = crud.vcn_response.get(db=db, public_id=response_id)
    if not vcn_response:
        raise HTTPException(status_code=404, detail="Response to vacancy "
                                                    "not found")
    if not crud.app_user.is_superuser(current_user) and \
            (crud.vcn_response.get_can_update(current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    vcn_response = crud.vcn_response.update(db=db,
                                            db_obj=vcn_response,
                                            obj_in=response_in)
    return vcn_response

