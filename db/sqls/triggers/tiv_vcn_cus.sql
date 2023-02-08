drop trigger if exists tiv_vcn_cus on v_vcn_cus;
create trigger tiv_vcn_cus
    instead of insert
    on v_vcn_cus
    for each row
execute procedure v_vcn_ti();

