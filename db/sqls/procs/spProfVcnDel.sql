drop function if exists spProfVcnDel;
create or replace function spProfVcnDel(
   _user_id uuid
  ,_ownlist text
  ,_vwrlist text
) returns void
    language sql
as $$
    delete from v_vcn_viewers vv
    where vv.user_id = _user_id
      and vv.vacancy_id in(
        select v.id from vacancy v
        where v.code in(
            select btrim(t) as comp
            from regexp_split_to_table(_vwrlist, ',') as t
        )
    );
    delete from v_vcn_owners vv
    where vv.user_id = _user_id
      and vv.vacancy_id in(
        select v.id from vacancy v
        where v.code in(
            select btrim(t) as comp
            from regexp_split_to_table(_ownlist, ',') as t
        )
    );
$$;
comment on function spProfVcnDel is 'Для профиля _user_id удалить связь(и) profile-vacancy по csv-перечню vacancy.code';