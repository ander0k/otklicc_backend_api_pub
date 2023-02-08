drop function if exists vacancy_taiu;
create or replace function vacancy_taiu() returns trigger
    language plpgsql
as
$$
declare _user_id uuid;
begin
    if new.company_id is not null then
        select c.owner_user_id into _user_id from company c where c.id = new.company_id;
        insert into vcn_user(user_id, vacancy_id, relation_role)
        values(_user_id, new.id, 'own')
        on conflict do nothing;
    end if;
    return NEW;
end;
$$;
