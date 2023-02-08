from uuid import UUID
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas, utils, json, core.config
from api import deps
from core.config import settings
from pathlib import Path
from tests.crud.test_user import test_update_user

router = APIRouter()


@router.get("/testmake")
def test_make(
        *,
        db: Session = Depends(deps.get_db),
        clean_only: bool = False
) -> Any:
    """
    Пересоздать данные для теста видимости Profiles
    """
    clean_only = 1 if clean_only else 0
    db.execute(f"call spMakeTest({clean_only});")
    db.commit()
    return "ok"

@router.put("/{public_id}")
def test_update(
        *,
        db: Session = Depends(deps.get_db),
        public_id: UUID,
) -> Any:
    """
    Изменение записи.
    """
    return "test_update: ok"


@router.get("/{public_id}",)
def read_vacancy(
        *,
        db: Session = Depends(deps.get_db),
        public_id: UUID,
) -> Any:
    """
    Получить запись по public_id.
    """
#    vacancy = crud.vacancy.get(db=db, public_id=public_id)
#    if not vacancy:
#        raise HTTPException(status_code=404, detail="Vacancy not found")
#    return vacancy
    # Run a database query.
    query_str = "select * from pg_stat_activity as pgact left join pg_stat_ssl pss on pgact.pid = pss.pid order by pgact.pid, pgact.backend_start;"

    result = db.execute(query_str)
    if result:
        query_result_row = result.fetchall()
    result.close()

    return {"stat_activity": query_result_row}


@router.get("/set/")
def info_set(*, db: Session = Depends(deps.get_db)) -> core.config.Settings:
    """
    Поглядеть все настройки config.settings
    """
    return settings

@router.get("/log/")
def show_log(*, db: Session = Depends(deps.get_db)) -> core.config.Settings:
    """
    Поглядеть uvicorn.log
    """
    with open('uvicorn.log') as f:
        contents = f.read()
    return contents

@router.get("/user_upd/")
def user_upd(*, db: Session = Depends(deps.get_db)):
    test_update_user(db)
    return None

