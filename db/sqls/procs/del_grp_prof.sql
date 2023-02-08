drop procedure if exists del_grp_prof;
create or replace procedure del_grp_prof(
     parent text
    ,child  text
)
as $$
begin
    if parent is not null then
        delete from grouptree
        where grp_class = 1 and name in (
            select btrim(t) as name
            from regexp_split_to_table(parent, ',') as t
        );
    end if;

    if child is not null then
        delete from professions
        where name in (
            select btrim(t) as name
            from regexp_split_to_table(child, ',') as t
        );
    end if;

end;
$$ language plpgsql;