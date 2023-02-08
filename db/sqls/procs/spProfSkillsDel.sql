drop procedure if exists spProfSkillsDel;
create procedure spProfSkillsDel(
    _user_id uuid
   ,_list text
) language sql
as $$
    update vcn_response set hidden = true
    where user_id = _user_id
      and demand_id in(
        select id from vcn_demand
        where metatag in(
            select btrim(t) as tag from regexp_split_to_table(_list, ',') as t
        )
    );
$$;
comment on procedure spProfSkillsDel is 'Для профиля _user_id скрыть skills по csv-перечню _list';