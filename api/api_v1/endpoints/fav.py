from typing import Any,List,Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import deps
from crud import crud_fav
from schemas import TokenData, FavOut, FavDel

router = APIRouter()


@router.get("/", response_model = List[FavOut])
def get_fav(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
) -> List[FavOut]:
    return crud_fav.fav.get(db=db, user_id=current_user.id)


@router.post("/", response_model = None)
def post_fav(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    fav: FavOut
) -> None:
    f = crud_fav.fav.get_by_name(db=db, user_id=current_user.id, fav_name=fav.name)
    if f:
        crud_fav.fav.update(db=db, user_id=current_user.id, fav=fav, new_name=None)
    else:
        return crud_fav.fav.create(db=db, user_id=current_user.id, fav=fav)


class Fav_Put(FavOut):
    new_name: Optional[str] = None

@router.put("/", response_model = None)
def put_fav(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    fav: Fav_Put,
) -> None:
    if fav.new_name:
        f = crud_fav.fav.get_by_name(db=db, user_id=current_user.id, fav_name=fav.new_name)
        if f:
            crud_fav.fav.destroy(db=db, user_id=current_user.id, fav=f)
    crud_fav.fav.update(db=db, user_id=current_user.id, fav=fav, new_name=fav.new_name)


@router.delete("/", response_model = None)
def delete_fav(*,
    db: Session = Depends(deps.get_db),
    current_user: TokenData = Depends(deps.check_current_user),
    fav: FavDel
) -> None:
    crud_fav.fav.destroy(db=db, user_id=current_user.id, fav=fav)


