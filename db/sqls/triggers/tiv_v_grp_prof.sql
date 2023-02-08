drop trigger if exists tiv_v_grp_prof on v_grp_prof;
create trigger tiv_v_grp_prof
    instead of insert
    on v_grp_prof
    for each row
execute procedure v_grp_prof_ti();

