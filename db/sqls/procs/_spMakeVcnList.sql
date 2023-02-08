drop function if exists _spMakeVcnList;
create or replace function _spMakeVcnList(_vacancy_id uuid, is_owners bool, _list text)
returns TABLE(mail text)
as $$
    declare row record;
    declare _user_id uuid;
    declare rrole text;
begin
    rrole = case when is_owners then 'own' else 'vwr' end;
    for row in select btrim(t) as mail from regexp_split_to_table(_list, ',') as t
    loop
        insert into app_user(email, utype, is_active) values(row.mail, 'HR', true)
        on conflict do nothing;
        select u.id into _user_id from app_user u where u.email = row.mail;

        insert into vcn_user(user_id, vacancy_id, relation_role)
        values(_user_id, _vacancy_id, rrole)
        on conflict do nothing
        returning user_id into _user_id;
        if _user_id is not null then
            mail = row.mail;
            return next;
        end if;
    end loop;
end;
$$ language plpgsql;
