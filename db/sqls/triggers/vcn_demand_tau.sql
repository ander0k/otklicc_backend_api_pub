drop function if exists vcn_demand_tau;
create or replace function vcn_demand_tau() returns trigger
    language plpgsql
as
$$
declare _uid uuid;
    declare _k smallint;
begin  --- проставить статус "рекомендовано" кому следует
    for _uid, _k in
        with s as ( -- user's skills
            select r.user_id, d.metatag as skill
            from vcn_response r
                     join vcn_demand d on r.demand_id = d.id
            where r.grade > 0
              and d.coefficient > 0
              and d.metatag is not null
        )
        select s.user_id, sum(sign(d.coefficient - 29.5))
        from vcn_demand d
        join s on s.skill = d.metatag
        where d.vacancy_id = old.vacancy_id
        group by s.user_id
    loop
        if _k >= 0 then
            insert into v_vcn_cus(user_id,vacancy_id,cus_status)
            values(_uid,old.vacancy_id,10);
        end if;
    end loop;
    return OLD;
end;
$$;
