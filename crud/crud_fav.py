from typing import Any,List
from uuid import UUID
from copy import copy
from fastapi import HTTPException
from core import config
from sqlalchemy import delete, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import between
from sqlalchemy.sql.functions import user
from crud.base import CRUDBase
from schemas import FavOut,FavPut,FavDel
from models import Fav


class CRUDFav(CRUDBase[Fav,FavPut,FavPut]):
    def get(self, db: Session, *, user_id: UUID) -> List[FavOut]:
        lst = []
        try:
            s = db.query(Fav).filter(Fav.owner == user_id).order_by(Fav.apply_time.desc()).all()
        finally:
            db.close()
        for fav in s:
            lst.append(FavOut(**fav.__dict__))
        return lst

    def get_by_name(self, db: Session, *, user_id: UUID, fav_name: str) -> Fav:
        try:
            fav = db.query(Fav).filter(and_(Fav.owner == user_id, Fav.name == fav_name)).first()
        finally:
            db.close()
        return fav

    def create(self, db: Session, *, user_id: UUID, fav: FavOut) -> None:
        db_obj = Fav(**fav.__dict__)
        db_obj.owner = user_id
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        finally:
            db.close()
        # return FavOut(**db_obj.__dict__)

    def update(self, db: Session, *, user_id: UUID, fav: FavOut, new_name: str) -> None:
        try:
            db_obj = db.query(Fav).filter(and_(Fav.owner == user_id, Fav.name == fav.name)).first()
            if not db_obj:
                raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
            obj_in = fav.dict(exclude_unset=True)
            obj_in['owner'] = db_obj.owner
            if new_name:
                obj_in['name'] = new_name
            obj = super().update(db=db, db_obj=db_obj, obj_in=obj_in)
        finally:
            db.close()
        # return FavOut(**obj.__dict__)

    def destroy(self, db: Session, *, user_id: UUID, fav: FavDel) -> None:
        try:
            stmt = delete(Fav).where(and_(Fav.owner == user_id, Fav.name == fav.name))
            db.execute(stmt)
            db.commit()
        finally:
            db.close()



fav = CRUDFav(Fav)

