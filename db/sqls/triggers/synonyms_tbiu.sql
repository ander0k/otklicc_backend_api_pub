drop function if exists synonyms_tbiu;
create or replace function synonyms_tbiu() returns trigger
    language plpgsql
as
$$
begin
    if TG_OP = 'INSERT' then
        new.synonyms = coalesce(new.synonyms, new.name);
    end if;
    if TG_OP = 'UPDATE' and left(new.synonyms, 1) = '+' then
        new.synonyms = coalesce(old.synonyms, '') ||' '|| substr(new.synonyms, 2);
        select string_agg(t, ' ') into new.synonyms
        from(
            select distinct row_number() OVER() as rn, t
            from regexp_split_to_table(new.synonyms, ' ') as t
            order by rn
        ) tt
        where t <> '';
    end if;
return NEW;
end;
$$;

comment on function synonyms_tbiu is 'Триггер для таблиц с полем synonyms';
