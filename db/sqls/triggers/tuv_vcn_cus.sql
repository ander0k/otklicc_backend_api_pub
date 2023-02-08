drop trigger if exists tuv_vcn_cus on v_vcn_cus;
create trigger tuv_vcn_cus
    instead of update
    on v_vcn_cus
    for each row
execute procedure v_vcn_cus_tu();

