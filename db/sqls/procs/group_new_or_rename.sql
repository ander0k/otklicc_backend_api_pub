drop function if exists group_new_or_rename;
create or replace function group_new_or_rename(
     class_id int
    ,old_name text
    ,new_name text
) returns uuid
as $$
declare _id uuid;
declare _nid uuid;
begin
    new_name = coalesce(new_name,old_name);
    select id into _nid from grouptree where grp_class = class_id and name = new_name;
    select id into _id  from grouptree where grp_class = class_id and name = old_name;
    if _nid is null then
        if _id is not null then  -- старая есть, новой нет: переименовать
            update grouptree set name = new_name where id = _id;
            return _id;
        else  -- нет ни старой, ни новой: создать
            insert into grouptree(grp_class, name)
            values(class_id, new_name)
            returning id into _id;
            return _id;
        end if;
    else --  новая есть
        if _id is null or _nid = _id then -- старой нет или это одна группа
            return _nid;
        end if;
        -- объединить две группы: перевязать child-ов старой на новую
        if class_id = 1 then
            update professions set node_id = _nid where node_id = _id;
        elsif class_id = 2 then
            update geos set node_id = _nid where node_id = _id;
        elsif class_id = 3 then
            update dmn_metatag set node_id = _nid where node_id = _id;
        end if;
        delete from grouptree where id = _id; -- удалить старую
    end if;
end;
$$ language plpgsql;
