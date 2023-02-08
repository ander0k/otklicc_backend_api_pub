from typing import Any,List,Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps
from crud import crud_dbconfig
from core import config
from core.config import Settings,TcDbInfo
from models.dbconfig import Tcdbinfo
from schemas import TokenData

router = APIRouter()


@router.get("/", response_model = Settings)
def get_Settings(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
) -> Settings:
    if not current_user.is_adm:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud_dbconfig.dbconfig.get(db=db)


@router.post("/", response_model = TcDbInfo)
def post_config(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    row: TcDbInfo
) -> None:
    if not current_user.is_adm:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud_dbconfig.dbconfig.create(db=db, row=row)


@router.put("/", response_model = TcDbInfo)
def put_config(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    row: TcDbInfo
) -> None:
    if not current_user.is_adm:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud_dbconfig.dbconfig.update(db=db, row=row)


@router.delete("/", response_model = None)
def delete_config(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    param_name: str
) -> None:
    if not current_user.is_adm:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    crud_dbconfig.dbconfig.destroy(db=db, param_name=param_name)


