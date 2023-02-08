from crud import crud_groups
from typing import Any,List
from copy import copy

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core import config
import crud
import schemas
from schemas.groups import TreeName,GroupPost,GroupPut,GroupDel
from api import deps

router = APIRouter()


@router.get("/", response_model = dict)
def get_group(*,
                db: Session = Depends(deps.get_db),
                current_user: schemas.TokenData = Depends(deps.check_current_user),
                group: TreeName
                ) -> dict:
    """
    Чтение групп
    """
    if not current_user.is_adm():
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.group.get_list(db=db, group=group)


@router.post("/", response_model = dict)
def new_group(*,
                db: Session = Depends(deps.get_db),
                current_user: schemas.TokenData = Depends(deps.check_current_user),
                group: GroupPost
                ) -> dict:
    """
    Добавление групп/элементов
    """
    if not current_user.is_adm():
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.group.post(db=db, group=group)


@router.put("/", response_model = dict)
def put_group(*,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    group: GroupPut
) -> dict:
    """
    Редактирование групп
    """
    if not current_user.is_adm():
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.group.put(db=db, group=group)


@router.delete("/", response_model = dict)
def del_group(*,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    group: GroupDel,
) -> dict:
    """
    Удаление групп/значений
    """
    if not current_user.is_adm():
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.group.delete(db=db, group=group)

