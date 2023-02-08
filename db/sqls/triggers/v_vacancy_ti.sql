drop function if exists v_vacancy_ti;
create or replace function v_vacancy_ti() returns trigger
    language plpgsql
as
$$
begin
    if new.company_id is null and new.company_code is not null then
        select id into new.company_id from company where code = new.company_code;
    end if;

    for i in 1..3 by 1 loop
        new.code = gen_short_code();
        exit when not exists(select 1 from vacancy where code = new.code);
    end loop;

    insert into vacancy(title,code,experience,leave_days,busyness,status,
                        salary_lo,salary_hi,currency,term,about,status_time,company_id)
    values(new.title,new.code,new.experience,new.leave_days,new.busyness,new.status,
           new.salary_lo,new.salary_hi,new.currency,new.term,new.about,new.status_time,new.company_id
    ) returning * into NEW;

    if new.demands is not null then
        insert into vcn_demand(vacancy_id,wording)
        select new.id, btrim(demand)
        from regexp_split_to_table(new.demands, ',') as demand;
    end if;

    if new.terms is not null then
        insert into vcn_terms(vcn_id, description)
        select new.id, btrim(descr)
        from regexp_split_to_table(new.terms, ',') as descr;
    end if;

    return NEW;
end;
$$;
