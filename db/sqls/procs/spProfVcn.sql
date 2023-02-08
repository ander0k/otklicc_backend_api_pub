drop function if exists spProfVcn;
create or replace function spProfVcn(
    _user_code text
   ,out vac_viewer_list json
   ,out vac_owner_list json
) as $$
    declare _uid uuid;
begin
    select id into _uid from app_user where code = _user_code;
    select json_object_agg(v.code,v.title) into vac_viewer_list
    from v_vcn_viewers vv
    join vacancy v on v.id = vv.vacancy_id
    where vv.user_id = _uid;

    select json_object_agg(v.code,v.title) into vac_owner_list
    from v_vcn_owners vv
    join vacancy v on v.id = vv.vacancy_id
    where vv.user_id = _uid;
end; $$ language plpgsql;
