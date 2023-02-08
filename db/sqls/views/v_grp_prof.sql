drop view if exists v_grp_prof;
create or replace view v_grp_prof
as
    select t.name parent_val,p.name child_val,p.synonyms syn
    from grouptree t
             left join professions p on p.node_id = t.id
    where t.grp_class = 1
;


