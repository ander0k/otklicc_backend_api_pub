drop procedure if exists _spMakeProfList;
create or replace procedure _spMakeProfList(_vacancy_id uuid, _list text)
as $$
    declare _prof text;
    declare _prof_id uuid;
begin
    for _prof in select btrim(t) from regexp_split_to_table(_list, ',') as t
    loop
        insert into professions(name) values(_prof)
        on conflict do nothing;
        select p.id into _prof_id from professions p where p.name = _prof;

        insert into vcn_prof(prof_id,vacancy_id)
        values(_prof_id, _vacancy_id)
        on conflict do nothing;
    end loop;
end;
$$ language plpgsql;
