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
from core.config import settings,Settings,TcDbInfo
from models.dbconfig import Tcdbinfo


class CRUDDbconfig(CRUDBase[Tcdbinfo,Tcdbinfo,Tcdbinfo]):
    def get(self, db: Session) -> Settings:
        result = Settings()
        try:
            info = db.query(Tcdbinfo).filter(Tcdbinfo.tag == 1).all()
        finally:
            db.close()
        for row in info:
            d = settings.__dict__.get(row.name, None)
            if row.name in settings.__dict__:
                if isinstance(d, bool):
                    v = row.value == "True"
                elif isinstance(d, int):
                    v = int(row.value)
                else:
                    v = row.value
                result.__dict__[row.name] = v
        return result

    def create(self, db: Session, *, row: Tcdbinfo) -> TcDbInfo:
        try:
            db.add(row)
            db.commit()
            db.refresh(row)
        finally:
            db.close()
        return row

    def update(self, db: Session, *, row: Tcdbinfo) -> TcDbInfo:
        db_obj = None
        try:
            db_obj = db.query(Tcdbinfo).filter(Tcdbinfo.name == row.name).first()
        finally:
            db.close()
        if not db_obj:
            raise HTTPException(status_code=config.EC_NOT_FOUND, detail=config.ER_NOT_FOUND)
        rc = super().update(db=db, db_obj=db_obj, obj_in=row)
        rt = TcDbInfo()
        rt.name = rc.name
        rt.tag = rc.tag
        rt.value = rc.value
        rt.mask = rc.mask
        return rt

    def destroy(self, db: Session, *, param_name: str) -> None:
        try:
            result = super().remove(db=db, id=param_name)
        finally:
            db.close()
        return result



dbconfig = CRUDDbconfig(Tcdbinfo)

