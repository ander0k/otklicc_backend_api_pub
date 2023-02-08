drop trigger if exists tiv_v_grp_tags on v_grp_tags;
create trigger tiv_v_grp_tags
    instead of insert
    on v_grp_tags
    for each row
execute procedure v_grp_tags_ti();

