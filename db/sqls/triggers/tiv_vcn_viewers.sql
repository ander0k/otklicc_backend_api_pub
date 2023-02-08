drop trigger if exists tiv_vcn_viewers on v_vcn_viewers;
create trigger tiv_vcn_viewers
    instead of insert
    on v_vcn_viewers
    for each row
execute procedure v_vcn_ti();

