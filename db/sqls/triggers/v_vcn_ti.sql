drop function if exists v_vcn_ti;
create or replace function v_vcn_ti() returns trigger
    language plpgsql
as
$$
declare _role text;
begin
    _role = case TG_TABLE_NAME
        when 'v_vcn_cus'     then 'cus'
        when 'v_vcn_viewers' then 'vwr'
        when 'v_vcn_owners'  then 'own'
        else null
    end;
    if _role is null then
        raise exception 'v_vcn_ti: unknown table';
    end if;
    new.id = null;
    insert into vcn_user(user_id,vacancy_id,relation_role,cus_status)
    values(new.user_id,new.vacancy_id,_role,coalesce(new.cus_status,0))
    on conflict(user_id,vacancy_id,relation_role) do NOTHING
    returning id into new.id;
    if _role = 'cus' and new.id is null then
        update v_vcn_cus set cus_status = new.cus_status
        where user_id = new.user_id and vacancy_id = new.vacancy_id
        returning id, cus_status into new.id, new.cus_status;
    end if;
    return NEW;
end;
$$;

comment on function v_vcn_ti() is 'instance trigger for views: v_vcn_cus, v_vcn_viewers, v_vcn_owners';
