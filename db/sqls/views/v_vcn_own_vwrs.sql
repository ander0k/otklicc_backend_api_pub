drop view if exists v_vcn_own_vwrs;
create or replace view v_vcn_own_vwrs
as
    select v.id,v.relation_role = 'own' is_own,v.vacancy_id,v.user_id
    from vcn_user v
    where v.relation_role in('own','vwr')
;
