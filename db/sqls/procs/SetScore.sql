drop function if exists SetScore;
create or replace function SetScore(
     _hr_id uuid
    ,_demand uuid
    ,_profile text
    ,_grade int
) returns bool
as $$
    declare _uid uuid;
    declare _vid uuid;
    declare _k smallint;
begin
    if not exists(
        select v.id
        from v_vcn_owners v
        join vcn_demand d on d.vacancy_id = v.vacancy_id
        where v.user_id = _hr_id
    ) then
        return false;
    end if;

    _uid = (select id from app_user where code = _profile);
    update vcn_response set
        grade = _grade,
        grader_id = _hr_id,
        grade_time = CURRENT_TIMESTAMP
    where demand_id = _demand
      and user_id = _uid;

    --- проставить статус 50 тем, у кого он 40
    _vid = (select d.vacancy_id from vcn_demand d join vcn_response r on r.demand_id = d.id
            where d.id = _demand and r.user_id = _uid);
    update vcn_user set cus_status = 50
    where relation_role = 'cus'
      and vacancy_id = _vid
      and user_id = _uid
      and cus_status = 40;

    return true;
end;
$$ language plpgsql;
