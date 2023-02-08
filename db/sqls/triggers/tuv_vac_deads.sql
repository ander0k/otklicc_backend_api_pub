drop trigger if exists tuv_vac_deads on v_vac_deads;
create trigger tuv_vac_deads
    instead of update
    on v_vac_deads
    for each row
execute procedure v_vac_deads_tu();

