drop view if exists v_grp_comps;
create or replace view v_grp_comps
as
    select coalesce(c.sub_name, '<Прочие компании>') parent_val,c.name child_val,c.synonyms syn
    from company c
    order by c.sub_name,c.name
;

