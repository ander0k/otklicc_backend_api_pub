drop trigger if exists tbiu_professions on professions;
create trigger tbiu_professions
    before insert or update
    on professions
    for each row
execute procedure synonyms_tbiu();

