drop view if exists v_notif_usr;
create or replace view v_notif_usr
as
    select distinct user_id,mailto,user_code
    from (
         select v.user_id,u.email mailto,u.code user_code,
             coalesce(current_date - --'2021-10-21',
                      (select max(mail_sended) from v_vcn_cus where v.user_id = v.user_id),
                      100) -
             case u.notifications
                 when 10 then 0
                 when 20 then 3
                 when 30 then 7
                 when 40 then 30
             end days
         from v_vcn_cus v
         join app_user u on v.user_id = u.id
         where v.cus_status = 10
           and v.mail_sended is null
           and u.notifications < 50
     ) w
    where days >= 0
;
comment on view v_notif_usr is 'CUS, для которых нужна рассылка писем-рекомендаций';