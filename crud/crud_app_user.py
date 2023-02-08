from typing import Any, Dict, Optional, Union, List
from sqlalchemy.dialects.postgresql.base import UUID
import copy

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models.app_user import AppUser
from schemas.app_user import AppUserComm, AppUserCreate, AppUserUpdate


class CRUDAppUser(CRUDBase[AppUser,AppUserCreate,AppUserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[AppUser]:
        result = None
        try:
            result = db.query(AppUser).filter(AppUser.email == email).first()
        finally:
            db.close()
        return result


    def get_by_emails(self, db: Session, *, emails: List[str]) -> Dict[str,AppUser]:
        result = {}
        try:
            for email in emails:
                result[email] = db.query(AppUser).filter(AppUser.email == email).first()
        finally:
            db.close()
        return result


    def get_by_code(self, db: Session, *, code: str) -> Optional[AppUser]:
        result = None
        try:
            result = db.query(AppUser).filter(AppUser.code == code).first()
        finally:
            db.close()
        return result

    def get_by_id(self, db: Session, *, id: str) -> Optional[AppUser]:
        result = None
        try:
            result = db.query(AppUser).filter(AppUser.id == id).first()
        finally:
            db.close()
        return result


    def create(self, db: Session, *, obj_in: AppUserCreate, isactive: bool=True) -> AppUser:
        db_obj = None
        try:
            db_obj = AppUser(
                code=obj_in.code,
                email=obj_in.email,
                passkey=get_password_hash(obj_in.password) if obj_in.password else None,
                utype = obj_in.utype,
                is_active = isactive
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        finally:
            db.close()
        return db_obj

    def update(
        self, db: Session, *, db_obj: AppUser, obj_in: Union[AppUserUpdate, Dict[str, Any]]
    ) -> AppUser:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        psw = update_data.get("password")
        if psw:
            passkey = get_password_hash(psw)
            update_data.pop("password", None)
            update_data["passkey"] = passkey
        result = None
        try:
            result = super().update(db, db_obj=db_obj, obj_in=update_data)
        finally:
            db.close()
        return result

    def destroy(self, db: Session, *, db_obj: AppUser):
        result = None
        try:
            result = super().remove(db=db, id=db_obj.id)
        finally:
            db.close()
        return result
    
    def remove(self, db: Session, *, db_obj: AppUser):
        result = {}
        if not db_obj.is_active and db_obj.deleted:
            return result
        update_data = AppUserUpdate(is_active=False, deleted=True)
        try:
            result = super().update(db, db_obj=db_obj, obj_in=update_data)
        finally:
            db.close()
        return result

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[AppUser]:
        app_user = self.get_by_email(db, email=email)
        if not app_user:
            return None
        if not verify_password(password, app_user.passkey):
            return None
        return app_user

    def is_active(self, app_user: AppUser) -> bool:
        return app_user.is_active and not app_user.deleted

    def is_superuser(self, app_user: AppUser) -> bool:
        return app_user.utype == 'ADM'


app_user = CRUDAppUser(AppUser)
