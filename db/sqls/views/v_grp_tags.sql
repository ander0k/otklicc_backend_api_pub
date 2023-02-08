drop view if exists v_grp_tags;
create or replace view v_grp_tags
as
    select t.name parent_val,m.name child_val,m.synonyms syn
    from grouptree t
    left join dmn_metatag m on m.node_id = t.id
    where t.grp_class = 3
;
