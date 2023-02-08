drop view if exists v_notif_vacs;
create or replace view v_notif_vacs
as
select vc.id,vc.user_id,v.code vac_code,v.title vac_title,
       c.code com_code,c.name com_name,c.logo_image com_img
from v_vcn_cus vc
         join vacancy v on v.id = vc.vacancy_id
         join company c on c.id = v.company_id
where vc.cus_status = 10
  and vc.mail_sended is null
;
