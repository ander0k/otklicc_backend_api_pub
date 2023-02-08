drop view if exists v_grp_geo;
create or replace view v_grp_geo
as
    select t.id grp_id,g.id geo_id,t.name parent_val,g.name child_val,g.synonyms syn
    from grouptree t
             left join geos g on g.node_id = t.id
    where t.grp_class = 2
;

