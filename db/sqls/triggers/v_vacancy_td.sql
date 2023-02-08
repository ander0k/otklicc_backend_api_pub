drop function if exists v_vacancy_td;
create or replace function v_vacancy_td() returns trigger
    language plpgsql
as
$$
begin
    delete from vacancy where id = old.id or code = old.code;
    return OLD;
end;
$$;
