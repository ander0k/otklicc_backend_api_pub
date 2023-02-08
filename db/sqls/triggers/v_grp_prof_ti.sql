drop function if exists v_grp_prof_ti;
create or replace function v_grp_prof_ti() returns trigger
    language plpgsql
as
$$
declare _class int;
    declare _tid uuid;
begin
    _class = 1;
    insert into grouptree(grp_class, name)
    values(_class,new.parent_val)
    on conflict do nothing;
    select t.id into _tid from grouptree t where t.grp_class = _class and t.name = new.parent_val;
    -- добавить профессию
    insert into professions(node_id, name, synonyms)
    values(_tid, new.child_val, new.syn)
    on conflict(name) do update set synonyms = '+'|| coalesce(new.syn, '')
    returning synonyms into new.syn;

    return NEW;
end;
$$;

comment on function v_grp_prof_ti() is 'instance trigger for view v_grp_prof';
