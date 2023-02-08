drop trigger if exists tiv_vacancy on v_vacancy;
create trigger tiv_vacancy
    instead of insert
    on v_vacancy
    for each row
execute procedure v_vacancy_ti();

