drop trigger if exists tbiu_dmn_metatag on dmn_metatag;
create trigger tbiu_dmn_metatag
    before insert or update
    on dmn_metatag
    for each row
execute procedure synonyms_tbiu();

