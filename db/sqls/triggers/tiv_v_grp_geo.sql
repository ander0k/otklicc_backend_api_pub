drop trigger if exists tiv_v_grp_geo on v_grp_geo;
create trigger tiv_v_grp_geo
    instead of insert
    on v_grp_geo
    for each row
execute procedure v_grp_geo_ti();

