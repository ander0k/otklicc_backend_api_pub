from typing import Any,Dict,Optional,List
from fastapi import HTTPException
from sqlalchemy.sql.expression import delete
from starlette import status

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.company import Company
from utils import list2csv
from schemas.company import CompanyCreate,CompanyUpdate


class CRUDCompany(CRUDBase[Company,CompanyCreate,CompanyUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Company]:
        try:
            result = db.query(Company).filter(Company.code == code).first()
        finally:
            db.close()
        return result

    def get_vwrlist(self, db: Session, *, company_id: str) -> dict:
        try:
            query = "select comp_viewer_list from spComp_vwrlist(:comp_id);"
            result = db.execute(query, {"comp_id": company_id})
            s = result.first()
            result.close()
        finally:
            db.close()
        return s['comp_viewer_list']

    def create(self, db: Session, *, company: Company) -> Company:
        try:
            db.add(company)
            db.commit()
            db.refresh(company)
        finally:
            db.close()
        return company

    def make_viewers(self, db: Session, *, company: Company, comp_viewer_list: List[str]):
        try:
            lst = list2csv(comp_viewer_list)
            query = "select string_agg(email,',') from spMakeViewers(:comp_id, :comp_viewer_list);"
            result = db.execute(query, {"comp_id": company.id, "comp_viewer_list": lst})
            s = result.first()
            if s: s = s[0]
            db.commit()
            result.close()
        finally:
            db.close()
        return s

    def update(self, db: Session, *, db_obj: Company, update_data: Company):
        try:
            rc = super().update(db, db_obj=db_obj, obj_in=update_data)
        finally:
            db.close()
        return rc

    def del_viewers(self, db: Session, *, company_id: str, viewer_list: List[str]):
        try:
            lst = list2csv(viewer_list)
            query = "call spCompProfDel(:id, :list);"
            db.execute(query, {"id": company_id, "list": lst})
            db.commit()
        finally:
            db.close()
        return None


company = CRUDCompany(Company)