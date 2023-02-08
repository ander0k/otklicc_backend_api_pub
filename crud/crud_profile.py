from crud import crud_app_user
import json
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from utils import obj2json,list2csv
import schemas
from schemas.profile import Profile,ProfileBase,ProfileDel
from models.app_user import AppUser


class CRUDProfile(CRUDBase[AppUser,AppUser,AppUser]):
    def get(self, db: Session, *, 
            app_user: AppUser, 
            current_user: schemas.TokenData = None
    ) -> dict:
        is_adm = False
        if current_user != None:
            is_adm = current_user.is_adm() or current_user.id == app_user.id

        profile = ProfileBase(**app_user.__dict__).__dict__
        # общая часть
        try:    profile['education'] = json.loads(app_user.educations)
        except: profile['education'] = None
        try:    profile['job'] = json.loads(app_user.jobs)
        except: profile['job'] = None
        try:
            #-------- все для HR ------------------
            if app_user.utype == 'HR':
                if is_adm:
                    profile['comp_view'] = app_user.comp_view
                if is_adm or app_user.comp_view:  #-- read lists
                    profile['comp_viewer_list'] = None
                    profile['vac_owner_list'] = None
                    profile['comp_owner_list'] = None
                    profile['vac_viewer_list'] = None
                #---- comp_viewer_list
                    query = "select own_comp, view_comp from spProfComps(:code);"
                    result = db.execute(query, {"code": app_user.code})
                    for row in result:
                        profile['comp_viewer_list'] = row['view_comp']
                        profile['comp_owner_list'] = row['own_comp']
                        break
                    result.close()
                #---- vac_xxx_list
                    query = "select vac_viewer_list, vac_owner_list from spProfVcn(:code);"
                    result = db.execute(query, {"code": app_user.code})
                    row = result.first()
                    result.close()
                    profile['vac_viewer_list'] = row['vac_viewer_list']
                    profile['vac_owner_list'] = row['vac_owner_list']
            #-------- все для CUS -----------------
            if app_user.utype == 'CUS':
                if is_adm:
                    profile['reqr_view'] = app_user.reqr_view
                if is_adm or app_user.reqr_view:  #-- read skills
                    profile['skills'] = None
                    query = '''
                        select distinct d.metatag
                        from vcn_response r
                        join vcn_demand d on r.demand_id = d.id
                        where r.user_id = :user_id and not r.hidden
                        and r.grade > 0 and d.coefficient > 0 and d.metatag is not null
                    '''
                    lst = []
                    result = db.execute(query, {"user_id": app_user.id})
                    s = result.fetchone()
                    while s:
                        lst.append(s[0])
                        s = result.fetchone()
                    result.close()
                    profile['skills'] = lst
        finally:
            db.close()
        return profile
            

    def remove(self, db: Session, *, app_user: AppUser, data_obj: ProfileDel):
        jobs = None
        educations = None
        try:
            if data_obj.job and app_user.jobs:
                a = json.loads(app_user.jobs)
                for key in data_obj.job: a.pop(key, None)
                jobs = obj2json(a)
            if data_obj.education and app_user.educations:
                a = json.loads(app_user.educations)
                for key in data_obj.education: a.pop(key, None)
                educations = obj2json(a)
            if jobs or educations:
                obj_in = {"id": app_user.id}
                if jobs: obj_in["jobs"] = jobs
                if educations: obj_in["educations"] = educations
                crud_app_user.app_user.update(db=db,db_obj=app_user, obj_in=obj_in)
            if data_obj.skills:
                query = "call spProfSkillsDel(:user_id, :skills);"
                db.execute(query, {
                    "user_id"  : app_user.id,
                    "skills"   : list2csv(data_obj.skills),
                })
                db.commit()
            if data_obj.comp_viewer_list or data_obj.vac_owner_list or data_obj.vac_viewer_list:
                query = "select spProfListsDel(:user_id,:comps,:owns,:vwrs);"
                db.execute(query, {
                    "user_id": app_user.id, 
                    "comps": list2csv(data_obj.comp_viewer_list),
                    "owns" : list2csv(data_obj.vac_owner_list),
                    "vwrs" : list2csv(data_obj.vac_viewer_list)
                })
                db.commit()
        finally:
            db.close()

    def HasReply(self, db: Session, current_user: schemas.TokenData, app_user: AppUser) -> bool:
        try:
            cus = current_user.id if current_user.utype == 'CUS' else app_user.id if app_user.utype == 'CUS' else None
            if not cus: return False
            hr = current_user.id if current_user.utype == 'HR' else app_user.id if app_user.utype == 'HR' else None
            if not hr: return False
            query = 'select spCheckResp(:cus,:hr);'
            result = db.execute(query, {"cus": cus, "hr": hr})
            s = result.first()
            result.close()
        finally:
            db.close()
        return s[0]


profile = CRUDProfile(AppUser)