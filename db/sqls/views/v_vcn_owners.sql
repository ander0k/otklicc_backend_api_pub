drop view if exists v_vcn_owners;
create or replace view v_vcn_owners
as
    select v.id,v.vacancy_id,v.user_id
    from vcn_user v
    where v.relation_role = 'own'
;
