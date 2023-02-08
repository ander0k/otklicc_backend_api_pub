from typing import Any,List
from uuid import UUID
from sqlalchemy.orm import Session
from schemas.result import ResultDel, ResultPut


class CRUDResult:
    def get(self, db: Session, *, 
            page_rows : int = 5,
            page      : int = 1,
            vac_id    : UUID,
    ) -> List:
        if not page or page < 1: page = 1
        if not page_rows: page_rows = 5
        page_rows = min(page_rows, 50)
        try:
            query = '''
                select
                    u.code       as profile_code
                    ,u.first_name as name
                    ,u.last_name  as last_name
                    ,u.img        as img_url
                    ,u.email      as email
                    ,sum(r.grade * d.coefficient) as grade_summ
                from vcn_response r
                join vcn_demand d on r.demand_id = d.id
                join app_user u on u.id = r.user_id
                where not r.is_draft
                  and d.vacancy_id = :vac_id
                group by 1,2,3,4,5
                order by 6 desc nulls last
                limit :page_rows offset :offset
            '''
            s = db.execute(query, {
                'page_rows' : page_rows,
                'offset'    : (page -1) * page_rows,
                'vac_id'    : vac_id,
            }).fetchall()

            query = '''
                select 2 * sum(d.coefficient) as max_grade_summ
                from vcn_demand d
                where d.vacancy_id = :vac_id
            '''
            mx = db.execute(query, {
                'vac_id'    : vac_id,
            }).first()

            s.append(mx)
        finally:
            db.close()
        return s

    def delete(self, db: Session, *,
            vac_id: UUID,
            cus_code: str,
    ) -> None:
        query = '''
            delete from vcn_response r
            where r.user_id = (select id from app_user where code = :cus_code)
            and r.demand_id in(
                select id from vcn_demand where vacancy_id = :vac_id
                )
        '''
        try:
            db.execute(query, {
                'vac_id'  : vac_id,
                'cus_code': cus_code,
            })
            db.commit()
        finally:
            db.close()
        return None

result = CRUDResult()
