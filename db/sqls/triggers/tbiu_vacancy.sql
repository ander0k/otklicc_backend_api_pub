drop trigger if exists tbiu_vacancy on vacancy;
create trigger tbiu_vacancy
    before insert or update
    on vacancy
    for each row
execute procedure vacancy_tbiu();

