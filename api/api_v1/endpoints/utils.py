from typing import Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic.networks import EmailStr

import models, schemas
from api import deps
from core.celery_app import celery_app
from utils import send_test_email, decode_token

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.AppUser = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    bgtasks: BackgroundTasks,
    email_list: str,
    background: bool = False,
) -> Any:
    """
    Test emails.
    """
    if background:
        send_test_email(email_list=email_list, bgtasks=bgtasks)
    else:
        send_test_email(email_list=email_list, bgtasks=None)
    return {"msg": "Test email sent"}


@router.get('/jwt-decode/', response_model=schemas.TokenData)
def jwt_decode(jwt: str) -> dict:
    try:
        return decode_token(jwt)
    except:
        raise HTTPException(status_code=400, detail='')
