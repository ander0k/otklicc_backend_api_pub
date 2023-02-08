drop function if exists spVacData;
create or replace function spVacData(
    _vcn_id uuid
   ,_candidate uuid
----
   ,out cus_status int
   ,out terms json
   ,out demands json
   ,out responses json
   ,out metatags json
   ,out coefficients json
   ,out applies int
)as $$
begin
    select count(distinct r.user_id)
    into applies
    from vcn_response r
    where not r.is_draft
      and r.demand_id in (select d.id from vcn_demand d where d.vacancy_id = _vcn_id)
    ;

    select json_object_agg(t.id, t.description)
    into terms
    from (
         select *
         from vcn_terms tt
         where tt.vcn_id = _vcn_id
         order by tt.created, tt.ord
    ) t;

    select
          json_object_agg(t.id, t.wording)
         ,json_object_agg(t.id, t.metatag)
         ,json_object_agg(t.id, t.coefficient)
    into demands,metatags,coefficients
    from (
        select d.id, d.wording, d.metatag, d.coefficient
        from vcn_demand d
        where d.vacancy_id = _vcn_id
        order by d.created, d.ord
    )t;

    if _candidate is not null then
        select c.cus_status
        into cus_status
        from v_vcn_cus c where c.vacancy_id = _vcn_id and c.user_id = _candidate;
        if coalesce(cus_status, 0) < 20 then
            select t.cus_status into cus_status
            from spCusStatusSet(_candidate, _vcn_id, null, 20) t;
        end if;

        select json_object_agg(d.id, r.content)
        into responses
        from vcn_response r
        join vcn_demand d on d.id = r.demand_id
        where r.user_id = _candidate
          and d.vacancy_id = _vcn_id
          and not r.is_draft;
    end if;
end;
$$ language plpgsql;