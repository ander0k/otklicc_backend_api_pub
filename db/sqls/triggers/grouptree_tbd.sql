drop function if exists grouptree_tbd;
create or replace function grouptree_tbd() returns trigger
    language plpgsql
as
$$
begin
    if old.id_own is null then
        return null;
    end if;
    return OLD;
end;
$$;
