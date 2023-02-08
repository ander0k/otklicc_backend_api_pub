from typing import Any,List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from api import deps
import crud
import schemas

router = APIRouter()

@router.get("/anon/", response_model = List)
def vac_search_anon(*,
    db: Session = Depends(deps.get_db),
    page_rows           : int = 5,
    page                : int = 1,
    professions         : str = None,
    parent_professions  : str = None,
    company             : str = None,
    parent_company      : str = None,
    geos                : str = None,
    parent_geos         : str = None,
    experience          : str = None,
    deadline            : bool = None,
    popular             : bool = None,
) -> List:
    return vac_search(
        db                 = db, 
        current_user       = None,
        page_rows          = page_rows,
        page               = page,
        professions        = professions,
        parent_professions = parent_professions,
        company            = company,
        parent_company     = parent_company,
        geos               = geos,
        parent_geos        = parent_geos,
        experience         = experience,
        deadline           = deadline,
        popular            = popular,
    )

def SplitStr(lst: str) -> List:
    if lst:
        return lst.split(',')
    else:
        return None

@router.get("/", response_model = List)
def vac_search(*,
    db: Session = Depends(deps.get_db),
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    page_rows           : int = 5,
    page                : int = 1,
    professions         : str = None,
    parent_professions  : str = None,
    company             : str = None,
    parent_company      : str = None,
    geos                : str = None,
    parent_geos         : str = None,
    experience          : str = None,
    deadline            : bool = None,
    popular             : bool = None,
) -> List:
    if not current_user:
        current_user = schemas.TokenData(utype='CUS')
    return crud.search.get(
        db                 = db,
        user               = current_user,
        page               = page,
        page_rows          = page_rows,
        professions        = SplitStr(professions),
        parent_professions = SplitStr(parent_professions),
        company            = SplitStr(company),
        parent_company     = SplitStr(parent_company),
        geos               = SplitStr(geos),
        parent_geos        = SplitStr(parent_geos),
        experience         = experience,
        deadline           = deadline,
        popular            = popular,
    )
