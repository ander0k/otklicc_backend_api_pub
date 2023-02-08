drop procedure if exists spEnableOtk;
create or replace procedure spEnableOtk(_user_id uuid)
as $$
begin
    update app_user set is_active = true where id = _user_id;
    -- удалить активные отклики, если есть такие же не активные
    delete from vcn_response ra
    where ra.user_id = _user_id
      and not ra.is_draft
      and exists(
            select 1
            from vcn_response rd
            where rd.user_id = _user_id
              and rd.demand_id = ra.demand_id
              and rd.is_draft
        );
    -- проставить cus_status в "есть отклик"
    insert into v_vcn_cus(user_id,vacancy_id,cus_status)
    select distinct _user_id,d.vacancy_id,40
    from vcn_response r
    join vcn_demand d on d.id = r.demand_id
    where r.user_id = _user_id and r.is_draft = true;
    -- активировать неактивные отклики
    update vcn_response set is_draft = false where user_id = _user_id;
end;
$$ language plpgsql;
comment on procedure spEnableOtk is 'Активировать профиль и все его отклики';
