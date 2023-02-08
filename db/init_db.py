from sqlalchemy.orm import Session

import crud, schemas
from core.config import settings
from db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.app_user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.AppUserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            utype='ADM',
        )
        user = crud.app_user.create(db, obj_in=user_in)  # noqa: F841
