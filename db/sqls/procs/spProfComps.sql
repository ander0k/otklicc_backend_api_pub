drop function if exists spProfComps;
create function spProfComps(_user_code text, out own_comp json, out view_comp json)
as $$
    declare _user_id uuid;
begin
    select u.id into _user_id from app_user u where u.code = _user_code;

    select json_object_agg(c.code,c.name) into own_comp
    from company c where c.owner_user_id = _user_id;

    select json_object_agg(c.code,c.name) into view_comp
    from company c
    join prof_company pc on pc.company_id = c.id
    where pc.user_id = _user_id;
end;
$$ language plpgsql;


