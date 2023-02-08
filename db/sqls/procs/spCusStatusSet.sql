drop function if exists spCusStatusSet;
create or replace function spCusStatusSet(
     _user_id uuid
    ,_vac_id  uuid
    ,bookmarked bool
    ,_status  int
) returns setof v_vcn_cus
as $$
    declare rec record;
begin
    if bookmarked is not null then
        _status = case when bookmarked then 30 else 20 end;
    end if;
    if _status is not null then
        insert into v_vcn_cus(vacancy_id,user_id,cus_status)
        values(_vac_id,_user_id,_status)
        returning * into rec;
    end if;
    return next rec;
end;
$$ language plpgsql;
comment on function spCusStatusSet is
'создать запись/установить значение cus_status в v_vcn_cus для пары user-vacancy;
если bookmarked задан, значение cus_status определяет он.';