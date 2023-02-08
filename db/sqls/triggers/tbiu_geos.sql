drop trigger if exists tbiu_geos on geos;
create trigger tbiu_geos
    before insert or update
    on geos
    for each row
execute procedure synonyms_tbiu();

