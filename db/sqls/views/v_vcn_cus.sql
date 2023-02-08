drop view if exists v_vcn_cus;
create or replace view v_vcn_cus
as
    select v.id,v.vacancy_id,v.user_id,v.cus_status,v.mail_sended
    from vcn_user v
    where v.relation_role = 'cus'
;
