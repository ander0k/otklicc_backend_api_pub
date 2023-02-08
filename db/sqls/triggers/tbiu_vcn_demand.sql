drop trigger if exists tbiu_vcn_demand on vcn_demand;
create trigger tbiu_vcn_demand
    before insert or update
    on vcn_demand
    for each row
execute procedure vcn_demand_tbiu();

