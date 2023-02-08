drop view if exists v_vcn_viewers;
create or replace view v_vcn_viewers
as
    select v.id,v.vacancy_id,v.user_id
    from vcn_user v
    where v.relation_role = 'vwr'
;
