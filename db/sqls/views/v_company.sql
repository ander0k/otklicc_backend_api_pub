drop view if exists v_company;
create or replace view v_company
as
    select c.*,
           u.email as owner_email,
           nullif(coalesce(u.last_name,'') ||' '|| coalesce(u.first_name,''),' ') as owner_name
    from otklicc.company c
    left join otklicc.app_user u on u.id = c.owner_user_id
;
