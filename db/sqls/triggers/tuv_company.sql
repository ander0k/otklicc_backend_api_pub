drop trigger if exists tuv_company on v_company;
create trigger tuv_company
    instead of update
    on v_company
    for each row
execute procedure v_company_tu();

