drop trigger if exists tdv_vacancy on v_vacancy;
create trigger tdv_vacancy
    instead of delete
    on v_vacancy
    for each row
execute procedure v_vacancy_td();

