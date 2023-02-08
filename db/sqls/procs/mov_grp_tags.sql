drop procedure if exists mov_grp_tags;
create or replace procedure mov_grp_tags(
     child  text
    ,parent text
    ,new_name text
)
as $$
    declare _pid uuid;
    declare _syn text;
begin
    -- group rename
    if child is null then
        _pid = group_new_or_rename(3,parent, new_name);
        return;
    end if;

    if parent is not null then -- make group if not exist
        _pid = group_new_or_rename(3,parent, parent);
    end if;

    if new_name is null then  -- сменить группу
        update dmn_metatag set node_id = coalesce(_pid, node_id)
        where name = child;
    else    -- change name
        select synonyms into _syn from dmn_metatag where name = child;
        _syn = coalesce(_syn, '');
        _pid = coalesce(_pid, '00000000-0000-0000-0000-000000000003');
        insert into dmn_metatag(node_id, name, synonyms)
        values(_pid, new_name, _syn)
        on conflict(name) do update set synonyms = '+'|| _syn;
        -- переключить foreign keys от child к new_name
        update vcn_demand set metatag = new_name where metatag = child;
        delete from dmn_metatag where name = child;
    end if;
end;
$$ language plpgsql;