drop function if exists v_vcn_cus_tu;
create or replace function v_vcn_cus_tu() returns trigger
    language plpgsql
as
$$
--  declare row record;
begin
    new.cus_status = case
        when coalesce(old.cus_status,0) < new.cus_status then new.cus_status
        when coalesce(old.cus_status,0) = 30 and new.cus_status = 20 then new.cus_status
        else coalesce(old.cus_status,0)
    end;
    update vcn_user set
        user_id = new.user_id,
        vacancy_id = new.vacancy_id,
        relation_role = 'cus',
        cus_status = new.cus_status
    where id = old.id
    returning id, cus_status into new.id, new.cus_status;
    return NEW;
end;
$$;

comment on function v_vcn_cus_tu() is 'instance trigger on update for v_vcn_cus';
