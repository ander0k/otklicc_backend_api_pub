from typing import Any,List
from uuid import UUID
from sqlalchemy.orm import Session
from schemas import TokenData
from schemas.vacancy import CompanyCard,VacancySearch,\
        STATUS_DRAFT, STATUS_MODER, STATUS_REJECT, STATUS_PUBLIC, STATUS_ARCHIVE


class SearchItem:
    company_card: CompanyCard
    vacancy_card: VacancySearch
    professions : str
    geos        : str
    cus_status  : int

def ListQuote(lst: List) -> str:
    if lst:
        return ','.join(list(map("'{}'".format, lst)))
    else:
        return None

class CRUDSearch:
    def get(self, db: Session, *, 
            user                : TokenData,
            page                : int = 1,
            page_rows           : int = 5,
            professions         : List[str] = None,
            parent_professions  : List[str] = None,
            company             : List[str] = None,
            parent_company      : List[str] = None,
            geos                : List[str] = None,
            parent_geos         : List[str] = None,
            experience          : str = None,
            deadline            : bool = None,
            popular             : bool = None,
    ) -> list:
        if not page or page < 1: page = 1
        if not page_rows: page_rows = 5
        page_rows = min(page_rows, 50)
        _exp = '1' if experience else 'null'
        if not experience: experience = 'null'
        query = ''' select
            c.name,c.code c_code,c.logo_image,c.color,c.sec_color,c.verified,
			v.code,v.title,v.experience,v.post_date,v.leave_days,v.deadline,
            v.busyness,v.view_count,v.status,v.salary_lo,v.salary_hi,v.currency,
            v.term,u.cus_status,c.status comp_status,
            case v.status when 50 then null else greatest(0, v.deadline - current_date) end as left_days,
            (select string_agg(p.name,',')
                from vcn_prof vp
                join professions p on p.id = vp.prof_id
                where vp.vacancy_id = v.id
                ) as professions,
            (select string_agg(g.name,',')
                from vcn_geo vg
                join geos g on g.id = vg.geo_id
                where vg.vacancy_id = v.id
                ) as geos
            from vacancy v
            inner join company c on c.id = v.company_id
            left  join vcn_user u on u.vacancy_id = v.id and u.user_id = :id
            where ({} is null or v.experience in ({}))
        '''.format(_exp,experience)
        if user.utype == 'CUS':
            query += '\n  and v.status in({},{})'.format(STATUS_PUBLIC,STATUS_ARCHIVE)
        elif user.utype == 'HR':
            query += '\n  and v.id in(select vacancy_id from v_vcn_own_vwrs where user_id = :id)'
        if company:
            query += '\n  and lower(c.name) in ({})'.format(ListQuote(company).lower())
        if parent_company:
            query += '\n  and lower(c.sub_name) in ({})'.format(ListQuote(parent_company).lower())
        if professions or parent_professions:
            query += '''
                and v.id in (
                    select vp.vacancy_id
                    from vcn_prof vp where'''
            if professions:
                query += '''
                    vp.prof_id in (select p.id from professions p
                        where lower(p.name) in ({})
                    )'''.format(ListQuote(professions).lower())
                if parent_professions:
                    query += '\n  and '
            if parent_professions:
                query += '''
                    vp.prof_id in (select gp.prof_id
                        from v_grp_prof gp
                        where lower(gp.parent_val) in ({})
                    )'''.format(ListQuote(parent_professions).lower())
            query += ')'
        if geos or parent_geos:
            query += '''
                and v.id in (
                    select vg.vacancy_id
                    from vcn_geo vg where
                '''
            if geos:
                query += '''
                    vg.geo_id in (select id from geos
                        where lower(name) in ({})
                    )'''.format(ListQuote(geos).lower())
                if parent_geos:
                    query += '\n  and '
            if parent_geos:
                query += '''
                    vg.geo_id in (select geo_id from v_grp_geo
                        where lower(parent_val) in ({})
                )'''.format(ListQuote(parent_geos).lower())
            query += ')\n'
        query += ' order by'
        sort = {False: 'asc', True: 'desc'}
        if popular != None:
            query += ' v.view_count {},'.format(sort[popular])
        if deadline != None:
            query += ' v.deadline {},'.format(sort[deadline])
        query += ' v.post_date desc, v.title\n'
        query += 'limit :page_rows offset :offset'
        try:
            q = db.execute(query, {
                'page_rows'         : page_rows,
                'offset'            : (page -1) * page_rows,
                'id'                : user.id,
                'exp'               : experience,
            })
            r = q.fetchall()
            q.close()
        finally:
            db.close()
        result = []
        for s in r:
            item = SearchItem()
            item.company_card = CompanyCard(**s)
            item.company_card.status = s['comp_status']
            item.company_card.code = s['c_code']
            item.vacancy_card = VacancySearch(**s)
            csv = s['professions']
            item.professions = csv.split(',') if csv else []
            csv = s['geos']
            item.geos = csv.split(',') if csv else []
            item.cus_status = s['cus_status']
            result.append(item)
        return result

search = CRUDSearch()
