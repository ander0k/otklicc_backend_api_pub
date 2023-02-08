drop function if exists spMakeViewers;
create or replace function spMakeViewers(_company_id uuid, _viewer_list text)
returns TABLE(email text)
as $$
    declare row record;
    declare _user_id uuid;
begin
    for row in select btrim(t) as mail from regexp_split_to_table(_viewer_list, ',') as t
    loop
        insert into app_user(email, utype, is_active) values(row.mail, 'HR', true)
        on conflict do nothing;
        select u.id into _user_id from app_user u where u.email = row.mail;

        insert into prof_company(user_id, company_id)
        values(_user_id, _company_id)
        on conflict do nothing
        returning user_id into _user_id;
        if _user_id is not null then
            email = row.mail;
            return next;
        end if;
    end loop;
end;
$$ language plpgsql;
