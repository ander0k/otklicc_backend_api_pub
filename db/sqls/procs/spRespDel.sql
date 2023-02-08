drop function if exists spRespDel;
create or replace function spRespDel(
     _vac_id uuid
    ,_user_id uuid
    ,_demands_list text
) returns bool
as $$
    declare row record;
begin

    for row in
        select d.id,d.vacancy_id
        from vcn_demand d
        join(
            select btrim(q)::uuid as demand
            from regexp_split_to_table(_demands_list, ',') as q
        ) t on t.demand = d.id
    loop
        if row.vacancy_id <> _vac_id then
            return false;
        end if;
        delete from vcn_response where (user_id, demand_id) = (_user_id, row.id);
    end loop;
    return true;
end;
$$ language plpgsql;