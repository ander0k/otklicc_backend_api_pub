drop procedure if exists spVacDataUpd;
create or replace procedure spVacDataUpd(
     _user_id uuid
    ,_vac_id uuid
    ,_demands text
    ,_terms text
    ,bookmarked bool
    ,_responses text
    ,_metatags text
    ,coefficients text
)as $$
    declare row record;
    declare _rsp bool;
    declare _grp text;
    declare _pid uuid;
    declare _r record;
    declare rn int;
begin
    if bookmarked is not null then
        perform spCusStatusSet(_user_id,_vac_id, bookmarked, null);
    end if;
    -- DEMANDS
    for row in
        select btrim(r.key) as id, r.value as content,row_number() OVER() as num
        from json_each_text(_demands::json) r -- {"content":"id",...}
    loop
        if char_length(row.id) < 5 then
            insert into vcn_demand(vacancy_id,ord,wording)
            values(_vac_id,row.num,row.content)
            on conflict do nothing;
        else
            begin
                update vcn_demand set wording = row.content
                where id = row.id::uuid;
            exception when unique_violation then
            end;
        end if;
    end loop;
    -- METATAGS
    if nullif(_metatags, '') is not null then
          -- select profession group name
        select t.name into _grp
        from vcn_prof p
        join professions f on p.prof_id = f.id
        join grouptree t on t.id = f.node_id
        where p.vacancy_id = _vac_id;
        if _grp is not null then
              -- добавить, если нету, группу метатегаов, одноименную группе профессий
            _pid = group_new_or_rename(3,null, _grp);
        end if;
        for _r in select * from json_each_text(_metatags::json) r -- {"demand_uid":"tagName",...}
        loop
            if _pid is not null then -- добавить, если нету, метатег; группа - одноименная группе профессий
                insert into dmn_metatag(name, node_id) values(_r.value, _pid) on conflict do nothing;
            end if;
            -- назначить метатег деманду
            update vcn_demand d set metatag = _r.value
            where d.id = _r.key::uuid;
        end loop;
    end if;
    -- COEFFICIENTS
    if nullif(coefficients, '') is not null then
        update vcn_demand d set coefficient = r.value::int
        from json_each_text(coefficients::json) r -- {"demand_uid":"coefficient",...}
        where r.key::uuid = d.id;
    end if;
    -- TERMS
    rn = 0;
    for row in
        select btrim(r.key) as id, r.value as content
        from json_each_text(_terms::json) r -- {"content":"id",...}
    loop
        rn = rn +1;
        if char_length(row.id) < 5 then
            insert into vcn_terms(vcn_id,ord,description)
            values(_vac_id,rn,row.content)
            on conflict do nothing;
        else
            begin
                update vcn_terms set description = row.content
                where id = row.id::uuid;
            exception when unique_violation then
            end;
        end if;
    end loop;

    -- RESPONSES
    _rsp = false;
    for row in
        select d.id, t.value as content
        from vcn_demand d
        join ( -- join _responses и реальных vcn_demand отсекает возможный мусор
            select cast(nullif(r.key,'') as uuid) as key, r.value
            from json_each_text(_responses::json) r
        ) t on t.key = d.id
    loop
        _rsp = true;
        insert into vcn_response(user_id,demand_id,content,is_draft)
        values(_user_id, row.id, row.content, false)
        on conflict(user_id, demand_id, is_draft) do update set content = row.content;
    end loop;
    if _rsp then
        perform spCusStatusSet(_user_id,_vac_id, null, 40);
    end if;
end;
$$ language plpgsql;
