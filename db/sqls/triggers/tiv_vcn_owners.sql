drop trigger if exists tiv_vcn_owners on v_vcn_owners;
create trigger tiv_vcn_owners
    instead of insert
    on v_vcn_owners
    for each row
execute procedure v_vcn_ti();

