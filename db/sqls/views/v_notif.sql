drop view if exists v_notif;
create or replace view v_notif
as
    select id,user_id,user_code,mailto,vacancy_id,vac_code,vac_title,com_code,com_name,com_img
    from (
        select vc.id,vc.user_id,u.code user_code,u.email mailto,vc.vacancy_id,v.code vac_code,
            v.title vac_title,c.code com_code,c.name com_name,c.logo_image com_img,
            coalesce(current_date -
                (select max(mail_sended) from v_vcn_cus where user_id = vc.user_id),
                100)
              - case u.notifications
                  when 10 then  0 -- без задержки
                  when 20 then  3 -- раз в три дня
                  when 30 then  7 -- раз в неделю
                  when 40 then 30 -- раз в месяц
                  else 1000000    -- никогда
                end
            days
        from v_vcn_cus vc
        join app_user u on vc.user_id = u.id
        join vacancy v on v.id = vc.vacancy_id
        join company c on c.id = v.company_id
        where vc.cus_status = 10     -- вакансия рекомендована
          and vc.mail_sended is null -- письма еще не было
          and u.notifications < 50  -- рассылка не запрещена
    ) w
    where days >= 0
;
comment on view v_notif is 'Пары user_id,vacancy_id для которых нужна рассылка писем-рекомендаций';