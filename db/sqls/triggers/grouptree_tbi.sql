drop function if exists grouptree_tbi;
create or replace function grouptree_tbi() returns trigger
    language plpgsql
as
$$
begin
    if new.id_own is null then
        new.id_own = case new.grp_class
            when 1 then '00000000-0000-0000-0000-000000000001'
            when 2 then '00000000-0000-0000-0000-000000000002'
            when 3 then '00000000-0000-0000-0000-000000000003'
            else null
        end;
        if new.id_own is not distinct from new.id then
            new.id_own = null;
        end if;
    end if;
    return NEW;
end;
$$;
