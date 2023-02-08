drop view if exists v_vacancy;
create or replace view v_vacancy
as
    select
       v.*
       ,case v.status when 50 then null
        else greatest(0, v.deadline - current_date)
        end as left_days
       ,(select string_agg(p.name,',')
         from vcn_prof vp
         join professions p on p.id = vp.prof_id
         where vp.vacancy_id = v.id
        ) as professions
       ,(select string_agg(g.name,',')
         from vcn_geo vg
         join geos g on g.id = vg.geo_id
         where vg.vacancy_id = v.id
        ) as geos
       ,c.name as company,c.code as company_code,
       (select json_object_agg(t.id, t.description) from
          (select * from vcn_terms tt where tt.vcn_id = v.id order by tt.ord) t
       )::text as terms,
       (select json_object_agg(t.id, t.wording)
          from (select d.id, d.wording from vcn_demand d
                where d.vacancy_id = v.id order by d.ord)t
       )::text as demands
    from otklicc.vacancy v
    left outer join otklicc.company c on c.id = v.company_id
;
