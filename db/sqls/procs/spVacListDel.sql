drop procedure if exists spVacListDel;
create procedure spVacListDel(
     vac_id uuid
    ,rrole text
    ,list  text
)
as $$
begin
    delete from vcn_user vu
    where vu.vacancy_id = vac_id
      and vu.relation_role = rrole
      and vu.user_id in (
        select u.id
        from app_user u
        where u.email in (
            select btrim(t) as mail from regexp_split_to_table(list, ',') as t
        )
    );
end;
$$ language plpgsql;