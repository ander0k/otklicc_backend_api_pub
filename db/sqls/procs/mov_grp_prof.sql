drop procedure if exists mov_grp_prof;
create or replace procedure mov_grp_prof(
     child  text
    ,parent text
    ,new_name text
)
as $$
    declare _id uuid;
    declare _pid uuid;
    declare _nid uuid;
    declare _syn text;
begin
    -- group rename
    if child is null then
        _pid = group_new_or_rename(1,parent, new_name);
        return;
    end if;

    if parent is not null then -- make group if not exist
        _pid = group_new_or_rename(1,parent, parent);
    end if;

    if new_name is null then  -- сменить группу
        update professions set
            node_id = coalesce(_pid, node_id)
        where name = child;
    else    -- change name
        select id into _nid from professions where name = new_name;
        if  _nid is null then
            -- new_name отсутствует, просто преименовать (и переместить, если есть parent)
            update professions set
                name = new_name, node_id = coalesce(_pid, node_id)
            where name = child;
        else -- merge professions:
            select id,synonyms into _id,_syn from professions where name = child;
            -- переключить foreign keys от _id к _nid
            update vcn_prof set prof_id = _nid where prof_id = _id;
            delete from professions where id = _id;
            update professions set synonyms = '+'|| _syn where id = _nid;
        end if;
    end if;
end;
$$ language plpgsql;