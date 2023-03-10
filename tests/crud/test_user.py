from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from core.security import verify_password
from schemas.app_user import AppUserCreate, AppUserUpdate
from tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = AppUserCreate(email=email, password=password)
    app_user = crud.app_user.create(db, obj_in=user_in)
    assert app_user.email == email
    assert hasattr(app_user, "passkey")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = AppUserCreate(email=email, password=password)
    app_user = crud.app_user.create(db, obj_in=user_in)
    authenticated_user = crud.app_user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert app_user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    app_user = crud.app_user.authenticate(db, email=email, password=password)
    assert app_user is None


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = AppUserCreate(email=email, password=password)
    app_user = crud.app_user.create(db, obj_in=user_in)
    is_active = crud.app_user.is_active(app_user)
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = AppUserCreate(email=email, password=password, disabled=True)
    app_user = crud.app_user.create(db, obj_in=user_in)
    is_active = crud.app_user.is_active(app_user)
    assert is_active


def test_check_if_user_is_superuser(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = AppUserCreate(email=email, password=password, is_superuser=True)
    app_user = crud.app_user.create(db, obj_in=user_in)
    is_superuser = crud.app_user.is_superuser(app_user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = AppUserCreate(email=username, password=password)
    app_user = crud.app_user.create(db, obj_in=user_in)
    is_superuser = crud.app_user.is_superuser(app_user)
    assert is_superuser is False


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = AppUserCreate(email=username, password=password, is_superuser=True)
    app_user = crud.app_user.create(db, obj_in=user_in)
    user_2 = crud.app_user.get(db, id=app_user.id)
    assert user_2
    assert app_user.email == user_2.email
    assert jsonable_encoder(app_user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = AppUserCreate(email=email, password=password, is_superuser=True)
    app_user = crud.app_user.create(db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = AppUserUpdate(password=new_password, is_superuser=True)
    crud.app_user.update(db, db_obj=app_user, obj_in=user_in_update)
    user_2 = crud.app_user.get(db, id=app_user.id)
    assert user_2
    assert app_user.email == user_2.email
    assert verify_password(new_password, user_2.passkey)
