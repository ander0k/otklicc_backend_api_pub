from typing import Any,List
from uuid import UUID
from sqlalchemy.orm import Session
from schemas.scoring import ScoringPut


class CRUDScoring:
    def get(self, db: Session, *, 
            page_rows : int = 5,
            page      : int = 1,
            vac_id    : UUID,
            demand    : UUID = None,
            scored    : bool = None,
    ) -> dict:
        if not page or page < 1: page = 1
        if not page_rows: page_rows = 5
        page_rows = min(page_rows, 50)
        query = '''
            select d.id
            from vcn_demand d
            where d.vacancy_id = :vac_id
            order by d.created, d.ord
        '''
        result = {}
        demands = []
        try:
            q = db.execute(query, {
                'vac_id' : vac_id,
            })
            s = q.fetchone()
            while s:
                if not demand: demand = s[0]
                demands.append(s[0])
                s = q.fetchone()
            q.close()
            result['demand'] = demand
            result['demands'] = demands

            query = 'select d.wording from vcn_demand d where d.id = :id'
            result['demand_content'] = \
            db.execute(query, {
                'id': demand
            }).scalar()
            
            query = '''
                select r.content, u.first_name as name,u.last_name,u.img img_url,u.code profile_code,r.grade
                from vcn_response r
                join app_user u on u.id = r.user_id
                where r.demand_id = :demand and not r.is_draft
            '''
            if scored != None:
                query = query + '  and r.grade is {} null\n'.format('not' if scored else '')
            query = query + 'limit :page_rows offset :offset'

            q = db.execute(query, {
                'page_rows' : page_rows,
                'offset'    : (page -1) * page_rows,
                'demand'    : demand,
            })
            result['responses'] = q.fetchall()
            q.close()
        finally:
            db.close()
        return result

    def put(self, db: Session, *,
            hr_id: UUID,
            scoring: ScoringPut,
    ) -> bool:
        try:
            query = 'select SetScore(:hr_id,:demand,:profile,:grade)'
            result = db.execute(query, {
                'hr_id': hr_id,
                'demand': scoring.demand,
                'profile': scoring.profile_code,
                'grade': scoring.grade
            }).scalar()
            db.commit()
        finally:
            db.close()
        return result

scoring = CRUDScoring()
