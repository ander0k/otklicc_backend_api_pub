drop procedure if exists _spMakeGeoList;
create or replace procedure _spMakeGeoList(_vacancy_id uuid, _list text)
as $$
    declare _geo text;
    declare _geo_id uuid;
begin
    for _geo in select btrim(t) from regexp_split_to_table(_list, ',') as t
    loop
        insert into geos(name) values(_geo)
        on conflict do nothing;
        select g.id into _geo_id from geos g where g.name = _geo;

        insert into vcn_geo(geo_id, vacancy_id)
        values(_geo_id, _vacancy_id)
        on conflict do nothing;
    end loop;
end;
$$ language plpgsql;
