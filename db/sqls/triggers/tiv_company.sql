drop trigger if exists tiv_company on v_company;
create trigger tiv_company
    instead of insert
    on v_company
    for each row
execute procedure v_company_ti();

