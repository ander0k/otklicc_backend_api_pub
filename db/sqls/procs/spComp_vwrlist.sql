drop function if exists spComp_vwrlist;
create function spComp_vwrlist(_company_id uuid, out comp_viewer_list json)
as $$
begin
    select json_object_agg(u.email, u.last_name || ' ' || u.first_name) into comp_viewer_list
    from app_user u
    join prof_company p on p.user_id = u.id
    where p.company_id = _company_id;
end;
$$ language plpgsql;

