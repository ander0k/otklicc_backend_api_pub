drop trigger if exists tau_vcn_demand on vcn_demand;
create trigger tau_vcn_demand
    after update
    on vcn_demand
    for each row
execute procedure vcn_demand_tau();

