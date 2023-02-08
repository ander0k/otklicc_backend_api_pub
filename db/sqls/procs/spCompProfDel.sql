drop procedure if exists spCompProfDel;
create procedure spCompProfDel(
   _company_id uuid
  ,mail_list text
)
as $$
begin
    delete from prof_company pc
    where pc.company_id = _company_id
      and pc.user_id in (
        select u.id
        from app_user u
        where u.email in (
            select btrim(t) as comp from regexp_split_to_table(mail_list, ',') as t
        )
    );
end;
$$ language plpgsql;
comment on procedure spCompProfDel is
'Для компании _company_id удалить связь(и) profile-company по csv-перечню app_user.email';