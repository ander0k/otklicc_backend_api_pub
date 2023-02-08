drop trigger if exists taiu_vacancy on vacancy;
create trigger taiu_vacancy
    after insert or update
    on vacancy
    for each row
execute procedure vacancy_taiu();

