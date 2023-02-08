drop function if exists vcn_demand_tbiu;
create or replace function vcn_demand_tbiu() returns trigger
    language plpgsql
as
$$
begin
    if new.metatag is not null then
        insert into dmn_metatag(name) values(new.metatag)
        on conflict do nothing;
    end if;
    return NEW;
end;
$$;
