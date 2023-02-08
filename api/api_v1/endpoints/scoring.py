from typing import Any,List
from core import config
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import deps
import crud
from schemas import TokenData, ScoringPut

router = APIRouter()


@router.get("/", response_model = dict)
def get_scoring(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    page_rows   : int = 5,
    page        : int = 1,
    code        : str,
    demand      : UUID = None,
    scored      : bool = None
) -> dict:
    if current_user.utype != 'HR':
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    vacancy = crud.vacancy.get_by_code(db=db, code=code)
    if not vacancy:
        raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
    vac_info = crud.vacancy.get_hrdata(db=db, vac_id=vacancy.id, inc_counter=False)
    if not current_user.email in vac_info.vac_owner_list:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.scoring.get(
        db        = db,
        page_rows = page_rows,
        page      = page,
        vac_id    = vacancy.id,
        demand    = demand,
        scored    = scored,
    )

@router.put("/", response_model = None)
def put_scoring(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    scoring: ScoringPut
) -> None:
    if not crud.scoring.put(db=db, hr_id=current_user.id, scoring=scoring):
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)


