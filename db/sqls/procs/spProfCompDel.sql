drop function if exists spProfCompDel;
create function spProfCompDel(
   _user_id uuid
  ,_list text
) returns void
    language sql
as $$
    delete from prof_company pc
    where pc.user_id = _user_id
      and pc.company_id in (
        select c.id
        from company c
        where c.code in (
            select btrim(t) as comp from regexp_split_to_table(_list, ',') as t
        )
    )
$$;
comment on function spProfCompDel is 'Для профиля _user_id удалить связь(и) profile-company по csv-перечню company.code';