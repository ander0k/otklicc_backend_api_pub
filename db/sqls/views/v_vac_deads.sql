drop view if exists v_vac_deads;
create or replace view v_vac_deads
as
  select v.id vac_id,v.deadline,greatest(0,deadline - current_date) left_days,v.mail_sended,
    v.code vac_code,v.title vac_title,c.code comp_code,c.name comp_title,v.status,
    ( select string_agg(u.email,',')
      from v_vcn_owners vv
      join app_user u on u.id = vv.user_id
      where vv.vacancy_id = v.id
    ) vac_owners
  from vacancy v
  left join company c on v.company_id = c.id
  where v.mail_sended < 2
    and (v.deadline <= current_date + 3 and v.status = 40
      or v.status = 50
      )
;
