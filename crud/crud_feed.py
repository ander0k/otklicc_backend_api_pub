from typing import Any,List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import between
from crud import crud_company, crud_vacancy
from schemas.feed import Feed, CompanyCard, VacancyCard


class CRUDFeed:
    def get(self, db: Session, *, 
            page_rows  : int = 5,
            page       : int = 1,
            user_id    : UUID,
            user_type  : str,
            role       : int = None,
            status     : int = None,
            cus_status : int = None,
    ) -> List[Feed]:
        if not page or page < 1: page = 1
        if not page_rows: page_rows = 5
        page_rows = min(page_rows, 50)

        where = []
        if user_type == 'CUS':
            where.append('v.status between 40 and 50')
            if cus_status:
                where.append(f'v.id in(select vacancy_id from v_vcn_cus where user_id = :user_id and cus_status = {cus_status})')
        elif status:
            where.append('v.status = :status')
        if user_type == 'HR':
            where.append('v.status is not null')
            if role == 10:
                where.append('v.id in(select vacancy_id from v_vcn_owners where user_id = :user_id)')
            elif role == 20:
                where.append('v.id in(select vacancy_id from v_vcn_viewers where user_id = :user_id)')
            else:
                where.append('v.id in(select vacancy_id from v_vcn_own_vwrs where user_id = :user_id)')
        query = '''
            select v.id,v.code,v.title,v.experience,v.post_date,v.leave_days,
                    case v.status when 50 then null else greatest(0, v.deadline - current_date) end as left_days,
                v.busyness,v.status,v.view_count,v.salary_lo,v.salary_hi,v.currency,v.term,v.company_id,
                (select string_agg(g.name,',')
                    from vcn_geo vg
                    join geos g on g.id = vg.geo_id
                    where vg.vacancy_id = v.id
                ) as geos
        '''
        if user_type == 'CUS':
            query += ',u.cus_status'
            where.append('u.user_id = :user_id')
        else:
            query += '''
                ,( select count(distinct r.user_id) from vcn_response r
                where not r.is_draft
                  and r.demand_id in (select d.id from vcn_demand d where d.vacancy_id = v.id)
                ) applies
            '''
        query += '\n from vacancy v'
        if user_type == 'CUS':
            query += '\n join vcn_user u on u.vacancy_id = v.id'
        w = '\n  and '.join(where)
        if w: w = ' where ' + w
        query += w + '''
            order by v.updated desc
            limit :page_rows offset :offset
        '''
        # print(query)
        try:
            q = db.execute(query, {
                'page_rows' : page_rows,
                'offset'    : (page -1) * page_rows,
                'user_id'   : user_id,
                'status'    : status,
                'role'      : role,
            })
            r = q.fetchall()
            q.close()
            lst = []
            for s in r:
                feed = Feed()
                feed.vacancy_card = VacancyCard(**s)
                company_id = str(s['company_id'])
                company = crud_company.company.get(db=db, id=company_id)
                feed.company_card = CompanyCard(**company.__dict__)
                if s['geos']:
                    feed.geos = s['geos'].split(',')
                status = s['status']
                if not status: status = 0
                if user_type == 'CUS':
                    feed.company_card.__dict__.pop('owner_email',None)
                    if status == 40 or status == 50:
                        feed.status = status
                    feed.cus_status = s['cus_status']
                else:
                    feed.company_card.comp_viewer_list = \
                        crud_company.company.get_vwrlist(db=db, company_id=company_id)
                    vac_info = crud_vacancy.vacancy.get_hrdata(db=db, vac_id=s['id'], inc_counter=False)
                    feed.vac_owner_list = vac_info.vac_owner_list
                    feed.vac_viewer_list = vac_info.vac_viewer_list
                    feed.applies = s['applies']
                    feed.status = status
                lst.append(feed)
        finally:
            db.close()
        return lst


feed = CRUDFeed()
