drop procedure if exists spNewResponses;
create or replace procedure spNewResponses(
     _user_id uuid
    ,_draft bool
    ,_responses json
    ,_metatags json
)as $$
    declare row record;
begin
    for row in
        select d.id, t.value as content
        from vcn_demand d
        join (
            select cast(key as uuid), value
            from json_each_text(_responses)
        ) t on t.key = d.id
    loop
        insert into vcn_response(is_draft,user_id,demand_id,content)
        values(_draft, _user_id, row.id, row.content)
        on conflict(user_id, demand_id, is_draft) do update set content = row.content;
    end loop;
end;
$$ language plpgsql;
