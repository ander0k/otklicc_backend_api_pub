drop function if exists vacancy_tbiu;
create or replace function vacancy_tbiu() returns trigger
    language plpgsql
as
$$
begin
    if TG_OP = 'INSERT' or new.status <> old.status then
        new.status_time = CURRENT_TIMESTAMP;
        new.status = abs(new.status);
        if new.status = 40 then -- опубликована
            new.post_date = CURRENT_TIMESTAMP;
        end if;
    end if;
    return NEW;
end;
$$;
