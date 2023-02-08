from typing import Any,List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import deps
from enum import Enum
from crud import crud_feed
from schemas import TokenData, Feed

router = APIRouter()


class Role(int, Enum):
    owners = 10
    viewers = 20


@router.get("/", response_model = List[Feed])
def get_feed(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    page_rows   : int = 5,
    page        : int = 1,
    role        : int = None,
    status      : int = None,
    cus_status  : int = None,
) -> List[Feed]:
    return crud_feed.feed.get(db=db,
        page_rows = page_rows,
        page = page,
        user_id = current_user.id,
        user_type = current_user.utype,
        role = role,
        status = status,
        cus_status = cus_status,
    )
