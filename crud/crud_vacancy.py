from typing import Any,List,Optional

from uuid import UUID
from fastapi import HTTPException
from core import config
from sqlalchemy.orm import Session
from copy import copy

from sqlalchemy.sql.functions import current_user
from utils import obj2json,list2csv

from crud.base import CRUDBase
from models.vacancy import Vacancy
from schemas.vacancy import VacancyCreate, VacancyUpdate, VacancyPost, VacancyGetInfo,\
        VacancyCardPost, VacancyPut, VacancyUpdInfo, VacancyNewInfo, VacancyDel


class VacPut(VacancyCreate):
    company_id: Optional[str] = None
    demands: Optional[str] = None
    terms: Optional[str] = None
    profession: Optional[str] = None
    geo: Optional[str] = None
    vac_owner_list: Optional[str] = None
    vac_viewer_list: Optional[str] = None

class CRUDVacancy(CRUDBase[Vacancy, VacancyCreate, VacancyUpdate]):
    def get(self, db: Session, *, id: str) -> Vacancy:
        try:
            result = db.query(Vacancy).filter(Vacancy.id == id).first()
        finally:
            db.close()
        return result

    def get_by_code(self, db: Session, *, code: str) -> Vacancy:
        try:
            result = db.query(Vacancy).filter(Vacancy.code == code).first()
        finally:
            db.close()
        return result

    def get_data(self, db: Session, *, vac_id: str, candidate_id: str) -> dict:
        try:
            query = "select cus_status, terms, demands, responses, metatags, coefficients, applies from spVacData(:vac_id, :candidate_id);"
            result = db.execute(query, {"vac_id": vac_id, "candidate_id": candidate_id})
            s = result.first()
            db.commit()
            result.close()
        finally:
            db.close()
        return s

    def get_hrdata(self, db: Session, *, vac_id: str, inc_counter: bool = False) -> VacancyGetInfo:
        try:
            query = "select view_count, vac_owner_list, vac_viewer_list from spVcnProf(:vac_id, :inc_counter)"
            # result = db.execute(query, {"vac_id": vac_id})
            result = db.execute(query, {"vac_id": vac_id, "inc_counter": inc_counter})
            row = result.first()
            result.close()
            if inc_counter:
                db.commit()
            info = VacancyGetInfo()
            if row:
                info.view_count = row['view_count']
                info.vac_owner_list = row['vac_owner_list']
                info.vac_viewer_list = row['vac_viewer_list']
        finally:
            db.close()
        return info

    def create(
        self, db: Session, *, obj_in: VacancyPost, company_id: str
    ) -> VacancyNewInfo:
        try:
            vacput = VacPut(**obj_in.vacancy_card.__dict__)
            vacput.company_id = company_id
            if obj_in.professions:
                vacput.profession = list2csv(obj_in.professions)
            if obj_in.geos:
                vacput.geo = list2csv(obj_in.geos)
            if obj_in.demands:
                vacput.demands = obj2json(obj_in.demands) # list2csv(obj_in.demands)
            if obj_in.terms:
                vacput.terms = obj2json(obj_in.terms) # list2csv(obj_in.terms)
            if obj_in.vac_owner_list:
                vacput.vac_owner_list = list2csv(obj_in.vac_owner_list)
            if obj_in.vac_viewer_list:
                vacput.vac_viewer_list = list2csv(obj_in.vac_viewer_list)
            query = '''select code,title,viewers,owners
                    from spVacancyNew(:company_id,:title,:status,:experience,:leave_days,
                    :busyness,:profession,:geo,:salary_lo,:salary_hi,:currency,:term,
                    :about,:demands,:terms,:vac_owner_list,:vac_viewer_list
                ) as id;'''
            result = db.execute(query, vacput.__dict__)
            row = result.first()
            db.commit()
            result.close()
            info = VacancyNewInfo()
            if row:
                info.code = row['code']
                info.title = row['title']
                info.vac_owner_list = row['owners']
                info.vac_viewer_list = row['viewers']
        finally:
            db.close()
        return info

    def new_responses(self, db: Session, *, user_id: str, draft: bool, responses: dict, metatags: dict) -> None:
        try:
            resp = obj2json(responses)
            tags = obj2json(metatags)
            query = "call spNewResponses(:user_id, :draft, :responses, :metatags);"
            db.execute(query, {"user_id": user_id, "draft": draft, "responses": resp, "metatags": tags})
            db.commit()
        finally:
            db.close()
        return None

    def otk_enable(self, db: Session, *, user_id: str) -> None:
        try:
            query = "call spEnableOtk(:user_id);"
            db.execute(query, {"user_id": user_id})
            db.commit()
        finally:
            db.close()
        return None

    def update(self, db: Session, *, user_id: str, vac_id: str, put_obj: VacancyPut) -> VacancyUpdInfo:
        query = """
            select viewers,owners from spVacancyUpd(:vac_id,:title,:professions,:status,:experience,:leave_days,
            :busyness,:geos,:salary_lo,:salary_hi,:currency,:term,:about,:vac_owner_list,:vac_viewer_list);
        """
        dct = copy(put_obj.vacancy_card.__dict__) if put_obj.vacancy_card else VacancyCardPost().__dict__
        dct['vac_id'] = vac_id
        dct["professions"] = list2csv(put_obj.professions)
        dct["geos"] = list2csv(put_obj.geos)
        dct["vac_owner_list"] = list2csv(put_obj.vac_owner_list)
        dct["vac_viewer_list"] = list2csv(put_obj.vac_viewer_list)
        try:
            result = db.execute(query, dct)
            row = result.first()
            db.commit()
            result.close()
            if put_obj.bookmarked != None or put_obj.demands or put_obj.terms or put_obj.responses or put_obj.metatags or put_obj.coefficients:
                query = f"call spVacDataUpd(:user_id,:vac_id,:demands,:terms,:bookmarked,:responses,:metatags,:coefficients);"
                db.execute(query, {"user_id": user_id, "vac_id": vac_id, "bookmarked": put_obj.bookmarked,
                    "demands"      : obj2json(put_obj.demands),
                    "terms"        : obj2json(put_obj.terms),
                    "responses"    : obj2json(put_obj.responses),
                    "metatags"     : obj2json(put_obj.metatags),
                    "coefficients" : obj2json(put_obj.coefficients),
                })
                db.commit()
            info = VacancyNewInfo()
            if row:
                info.vac_owner_list = row['owners']
                info.vac_viewer_list = row['viewers']
        finally:
            db.close()
        return info

    def remove(self, db: Session, *, vac_id: UUID, cus_id: UUID, vacancy: VacancyDel) -> None:
        try:
            if vacancy.responses:  # user is CUS
                query = 'select spRespDel(:vac_id,:user_id,:vac_list);'
                dct = {
                    'vac_id' : vac_id,
                    'user_id': cus_id,
                    'vac_list': list2csv(vacancy.responses)
                }
                result = db.execute(query, dct)
                ok = result.first()[0]
                db.commit()
                result.close()
                if not ok:
                    raise HTTPException(status_code=config.EC_BAD_PARAMS, detail='Demand не из этой вакансии')
            else:
                if vacancy.destroy_all:
                    return super().remove(db=db, id=vac_id)
                vacancy.professions = list2csv(vacancy.professions)
                vacancy.geos = list2csv(vacancy.geos)
                vacancy.vac_owner_list = list2csv(vacancy.vac_owner_list)
                vacancy.vac_viewer_list = list2csv(vacancy.vac_viewer_list)
                vacancy.terms = list2csv(vacancy.terms)
                vacancy.demands = list2csv(vacancy.demands)
                dct = vacancy.__dict__
                dct['vac_id'] = vac_id
                query = 'call spVacancyDel(:vac_id,:professions,:geos,:vac_owner_list,:vac_viewer_list,:terms,:demands);'
                db.execute(query, dct)
                db.commit()
        finally:
            db.close()
        return {}



    def get_multi_by_owner(
        self, db: Session, *, record_owner_id: UUID, skip: int = 0,
            limit: int = 100
    ) -> List[Vacancy]:
        """
        получить список вакансий, связанных с пользователем (группой)
        :param db:
        :param record_owner_id: публичный идентификатор пользователя (группы)
        :param skip:
        :param limit:
        :return:
        """
        try:
            rc =  (
                db.query(self.model)
                .filter(Vacancy.record_owner_id == record_owner_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        finally:
            db.close()
        return rc

    def get_multi_by_company(
        self, db: Session, *, company_id: UUID, skip: int = 0,
            limit: int = 100
    ) -> List[Vacancy]:
        """
        Получить все вакансии по организации
        :param db:
        :param company_id: публичный идентификатор организации
        :param skip: с...
        :param limit: по...
        :return:
        """
        try:
            rc = (
                db.query(self.model)
                .filter(Vacancy.company_id == company_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        finally:
            db.close()
        return rc

vacancy = CRUDVacancy(Vacancy)
