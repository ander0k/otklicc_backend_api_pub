import logging
from fastapi import BackgroundTasks
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from db.session import SessionLocal

import emails, schemas, json
from emails.template import JinjaTemplate
from jose import jwt

from core.config import settings
from sqlalchemy.orm import Session
import models
from core.security import create_access_token
from models import Vacancy, CronVac


def obj2json(obj: Any) -> str:
    if not obj: return None
    return json.dumps(obj=obj, ensure_ascii=False)


def list2csv(lst: Any) -> str:
    if not lst: return None
    return ','.join(lst)


def hr_front_host() -> str:
    url = urlparse(settings.FRONT_HOST)
    url = url._replace(netloc='hr.'+ url.netloc)
    return url.geturl()


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    email_to = email_to.strip()
    if email_to == '':
        print('==!! WARN: empty email_to')
        return
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    else:
        smtp_options["tls"] = False
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    else:
        smtp_options["user"] = ''
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    else:
        smtp_options["password"] = ''
    response = message.send(to=email_to.split(','), render=environment, smtp=smtp_options)
    debug_info = environment.get("debug_info")
    if debug_info:
        print(f"========= mail [{debug_info}] sended: {email_to} =========")
    logging.info(f"send email result: {response}")


def send_test_email(
    bgtasks: BackgroundTasks, # may be None
    email_list: str
) -> None:
    subject = f"{settings.PROJECT_NAME} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    if bgtasks == None:
        for email in email_list.split(","):
            send_email(
                email_to=email,
                subject_template=subject,
                html_template=template_str,
                environment={"project_name": settings.PROJECT_NAME, "email": email, "debug_info": "test_email"},
            )
    else:
        for email in email_list.split(","):
            bgtasks.add_task(send_email,
                email_to=email,
                subject_template=subject,
                html_template=template_str,
                environment={"project_name": settings.PROJECT_NAME, "email": email, "debug_info": "test_email"},
            )

############################## background mails ##################################

def send_reset_password_email(
    bgtasks: BackgroundTasks, 
    email_to: str, 
    email: str, 
    utype: str,
    token: str
) -> None:
    # project_name = settings.PROJECT_NAME
    subject = f"Восстановление пароля"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html"
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    front_host = settings.FRONT_HOST
    utype = utype.lower()
    if utype == 'hr' or utype == 'adm':
        url = urlparse(front_host)
        url = url._replace(netloc= utype +'.'+ url.netloc)
        front_host = url.geturl()
    link = f"{front_host}/?overlay=restore&token={token}"
    bgtasks.add_task(send_email,
    # send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(
    bgtasks: BackgroundTasks, 
    email_to: str,
    username: str, 
    is_hr: bool, 
    token: str
) -> None:
    # project_name = settings.PROJECT_NAME
    subject = f"Завершение регистрации"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html"
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    front_host = settings.FRONT_HOST
    if is_hr:
        url = urlparse(front_host)
        url = url._replace(netloc='hr.'+ url.netloc)
        front_host = url.geturl()
    link = f"{front_host}/?action=reg&token={token}"
    bgtasks.add_task(send_email,
    # send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_confirm_responce_email(
    bgtasks: BackgroundTasks, 
    email_to: str, 
    username: str, 
    vac: Vacancy, 
    token: str
) -> None:
    # project_name = settings.PROJECT_NAME
    subject = f"Подтверждение отклика"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / "anon_response.html"
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    front_host = settings.FRONT_HOST
    link = f"{front_host}/vacancy/{vac.code}/?action=otklik&token={token}"
    bgtasks.add_task(send_email,
    # send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "vacancy_name": vac.title,
            "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_interview_email(
    bgtasks: BackgroundTasks,
    email_to: str,
    vac_code: str,
    vacancy_title: str,
    company_code: str,
    company_name: str,
    hr_name: str,
    hr_last_name: str,
    hr_email: str,
    content: str
) -> None:
    subject = 'Приглашение на собеседование в компанию "{}"'.format(company_name)
    fn = "interview_invitation.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    front_host = settings.FRONT_HOST
    link = f"{front_host}/vacancy/{vac_code}/"
    company_link = f"{front_host}/company/{company_code}/"
    bgtasks.add_task(send_email,
    # send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "link": link, 
            "content": content,
            "vacancy_title": vacancy_title,
            "hr_name": hr_name,
            "hr_last_name": hr_last_name,
            "company_link": company_link,
            "company_name": company_name,
            "hr_email": hr_email,
        },
    )

############################## no background mails (from crone) ##################################

def send_vacancy_add_list_email(
    emails_to: str,
    tokens: dict, # пара email-token; элементов может быть больше, чем в emails_to
    vacancy_name: str, 
    vacancy_code: str, 
    asowner: bool,
) -> None:
    # project_name = settings.PROJECT_NAME
    subject = "Предоставление прав"
    fn = "vacancy_add_owner.html" if asowner else "vacancy_add_viewer.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    link = f"{hr_front_host()}/vacancy/{vacancy_code}/?action=approve&token="
    print('-->-------- vacancy_add_list sending to '+ emails_to +'---------')
    for email in emails_to.split(','):
        email = email.strip()
        if email == '':
            continue
        send_email(
            email_to=email,
            subject_template=subject,
            html_template=template_str,
            environment={
                "vacancy_name": vacancy_name,
                "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
                "link": link + tokens[email],
                "debug_info": "vacancy_add_list",
            },
        )


def send_comp_add_list_email(
    emails_to: str,
    tokens: dict, # пара email-token; элементов может быть больше, чем в emails_to
    company_name: str, 
    company_code: str, 
    asowner: bool,
) -> None:
    # project_name = settings.PROJECT_NAME
    subject = "Предоставление прав"
    fn = "company_add_owner.html" if asowner else "company_add_viewer.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    link = f"{hr_front_host()}/company/{company_code}/?action=approve&token="
    print('-->-------- company_add_list sending to '+ emails_to +'---------')
    for email in emails_to.split(','):
        email = email.strip()
        if email == '':
            continue
        send_email(
            email_to=email,
            subject_template=subject,
            html_template=template_str,
            environment={
                "company_name": company_name,
                "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
                "link": link + tokens[email],
                "debug_info": "company_add_list",
            },
        )


def send_comp_emails(
    emails_to: str,
    tokens: dict, # пара email-token
    company_name: str,
    company_code: str,
    asowner: bool,
    old_own: dict,
    new_own: dict,
) -> None:
    if emails_to:
        send_comp_add_list_email(
            emails_to=emails_to,
            tokens=tokens,
            company_name=company_name,
            company_code=company_code,
            asowner=asowner,
        )
    if old_own:
        send_comp_owner_email(
            email_to=old_own["email"],
            token=old_own["token"],
            company_name=company_name,
            company_code=company_code,
            is_new=False
        )
    if new_own:
        send_comp_owner_email(
            email_to=new_own["email"],
            token=new_own["token"],
            company_name=company_name,
            company_code=company_code,
            is_new=True
        )


def send_comp_owner_email(
    email_to: str,
    token: str,
    company_name: str,
    company_code: str,
    is_new: bool,
) -> None:
    # project_name = settings.PROJECT_NAME
    subject = "Передача прав"
    if is_new:
        fn = "company_add_owner.html"
        debug_info = 'company_add_owner'
        link = f"{hr_front_host()}/company/{company_code}/?action=approve&token={token}"
    else:
        fn = "company_delete_owner.html"
        link = ''
        debug_info = 'company_delete_owner'
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "company_name": company_name,
            "valid_hours": settings.EMAIL_TOKEN_EXPIRE_HOURS,
            "link": link,
            "debug_info": debug_info,
        },
   )


def send_recomend_email(
    mailto: str,
    token: str,
    vacs: List[CronVac],
) -> None:
    front_host = settings.FRONT_HOST
    fn = "vac_recom_row.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    lst = []    
    for vac in vacs:
        com_img = vac.com_img
        if com_img:
            n = com_img.find('/company/')
            pre = com_img[0:n]
            r = pre.rfind('/')
            pre = pre[0:r]
            com_img = pre +'/120'+ com_img[n:]
        lst.append(template_str.format(
            front_host = front_host,
            com_code =vac.com_code,
            vac_code = vac.vac_code,
            com_img = com_img,
            com_name = vac.com_name,
            vac_title = vac.vac_title,
        ))
    subject = "Рекомендованные вакансии"
    fn = "vac_recomendations.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    send_email(
        email_to=mailto,
        subject_template=subject,
        html_template=template_str,
        environment={
            "front_host": front_host,
            "token": token,
            "data_rows": "\n".join(lst),
            "debug_info": 'vac_recomendations',
        },
    )


def send_dedline_mail(     # send mail to HR за 3 дня до смерти
    email_to: str, 
    vac_code: str,
    vac_title: str,
    comp_code: str,
    comp_title: str,
):
    fn = "deadline.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=f'Дедлайн вакансии "{vac_title}"',
        html_template=template_str,
        environment={
            "front_host": settings.FRONT_HOST,
            "vac_code": vac_code,
            "vac_title": vac_title,
            "comp_code": comp_code,
            "comp_title": comp_title,
        },
    )


def send_vac_archive_mail(  # send mail to HR в день смерти
    email_to: str, 
    vac_code: str,
    vac_title: str,
    comp_code: str,
    comp_title: str,
):
    fn = "archive.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    link = f"{hr_front_host()}"
    send_email(
        email_to=email_to,
        subject_template=f'Вакансия "{vac_title}" перемещена в архив',
        html_template=template_str,
        environment={
            "link": link,
            "vac_code": vac_code,
            "vac_title": vac_title,
            "comp_code": comp_code,
            "comp_title": comp_title,
        },
    )


def send_feedback_mail(
    email_to: str, 
    vac_code: str,
    vac_title: str,
    comp_code: str,
    comp_title: str,
    percent: str,
    skills: List,
):
    fn = "feedback.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    lst = []
    for skill in skills:
        lst.append(f"\t<li> {skill} </li>\n")
    send_email(
        email_to=email_to,
        subject_template=f'Работодатель оценил ваш отклик на вакансию "{vac_title}"',
        html_template=template_str,
        environment={
            "front_host": settings.FRONT_HOST,
            "vac_code": vac_code,
            "vac_title": vac_title,
            "comp_code": comp_code,
            "comp_title": comp_title,
            "percent": f"хуже {100 - percent}%" if percent < 50 else f"лучше {percent}%",
            "skills": "\n".join(lst),
        },
    )


def send_zero_feedback_mail(
    email_to: str, 
    vac_code: str,
    vac_title: str,
    comp_code: str,
    comp_title: str,
):
    fn = "zero_feedback.html"
    fn = Path(settings.EMAIL_TEMPLATES_DIR) / fn
    with open(fn, "r", encoding="utf-8") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=f'Работодатель не оценил ваш отклик на вакансию "{vac_title}"',
        html_template=template_str,
        environment={
            "front_host": settings.FRONT_HOST,
            "vac_code": vac_code,
            "vac_title": vac_title,
            "comp_code": comp_code,
            "comp_title": comp_title,
        },
    )

#########################################################

def generate_password_reset_token(user: models.app_user.AppUser, expires_delta: timedelta = None) -> str:
    return create_access_token(subject=user.id,code=user.code,utype=user.utype,email=user.email,expires_delta=expires_delta)


def decode_token(token: str) -> schemas.TokenData:
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    # if decoded_token['sub'] != decoded_token.get('email'):
    decoded_token['id'] = decoded_token['sub']
    return decoded_token


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token['email']
    except jwt.JWTError:
        return None


def init_settings():
    db = SessionLocal()
    try:
        result = db.execute('select name,value from tcdbinfo where tag = 1')
        if result:
            rows = result.fetchall()
        result.close()
    finally:
        db.close()
    if rows:
        for row in rows:
            v = row['value']
            n = row['name']
            d = settings.__dict__.get(n, None)
            if n in settings.__dict__:
                if isinstance(d, bool):
                    v = bool(v)
                elif isinstance(d, int):
                    v = int(v)
                settings.__dict__[n] = v

