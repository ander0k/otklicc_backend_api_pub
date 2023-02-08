drop function if exists spCheckResp;
create or replace function spCheckResp(
     _cus uuid
    ,_hr  uuid
) returns bool language sql
as $$
    select exists(
      select 1
      from vcn_response cus
      join vcn_demand d on d.id = cus.demand_id
      join v_vcn_own_vwrs vv on vv.vacancy_id = d.vacancy_id
      where not cus.is_draft
        and cus.user_id = _cus
        and vv.user_id = _hr
   );
$$;
