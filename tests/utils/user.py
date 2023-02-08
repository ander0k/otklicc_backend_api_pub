from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import crud
from core.config import settings
from models.app_user import AppUser
from schemas.app_user import AppUserCreate,AppUserUpdate,AppUserBase
from tests.utils.utils import random_email, random_lower_string


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = AppUserCreate(username=email, email=email, password=password)
    app_user = crud.app_user.create(db=db, obj_in=user_in)
    return app_user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    app_user = crud.app_user.get_by_email(db, email=email)
    if not app_user:
        user_in_create = AppUserCreate(username=email, email=email, password=password)
        app_user = crud.app_user.create(db, obj_in=user_in_create)
    else:
        user_in_update = AppUserUpdate(password=password)
        app_user = crud.app_user.update(db, db_obj=app_user, obj_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
