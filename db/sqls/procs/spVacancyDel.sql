drop procedure if exists spVacancyDel;
create or replace procedure spVacancyDel(
     vac_id uuid
    ,prof_list text
    ,geo_list text
    ,vac_owner_list  text
    ,vac_viewer_list text
    ,terms text
    ,demands text
)
as $$
begin
    call spVacListDel(vac_id, 'own', vac_owner_list);
    call spVacListDel(vac_id, 'vwr', vac_viewer_list);

    delete from vcn_prof vp
    where vp.vacancy_id = vac_id
      and vp.prof_id in(
        select p.id
        from professions p
        join (
            select btrim(t) as prof from regexp_split_to_table(prof_list, ',') as t
        ) q on q.prof = p.name
    );

    delete from vcn_geo vg
    where vg.vacancy_id = vac_id
      and vg.geo_id in(
        select g.id
        from geos g
        join (
            select btrim(t) as geo from regexp_split_to_table(geo_list, ',') as t
        ) q on q.geo = g.name
    );

    delete from vcn_terms m
    where m.id in(
        select btrim(t)::uuid as id from regexp_split_to_table(terms, ',') as t
    );

    delete from vcn_demand d
    where d.id in(
        select btrim(t)::uuid as id from regexp_split_to_table(demands, ',') as t
    );

end;
$$ language plpgsql;