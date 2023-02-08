drop function if exists spVcnProf;
create or replace function spVcnProf(
     _vcn_id uuid
    ,inc_counter bool
---
    ,out view_count integer
    ,out vac_owner_list json
    ,out vac_viewer_list json
)
as $$
    declare row record;
begin
    if inc_counter then
        update vacancy set view_count = vacancy.view_count + 1
        where id = _vcn_id
        returning vacancy.view_count into view_count;
    else
        select v.view_count into view_count
        from vacancy v where id = _vcn_id;
    end if;
    for row in
        select  vu.relation_role as rrole, jsonb_object_agg(u.email, u.last_name ||' '|| u.first_name) as mails
        from vcn_user vu
                 join vacancy v on vu.vacancy_id = v.id
                 join app_user u on u.id = vu.user_id
        where v.id = _vcn_id
          and vu.relation_role in('vwr','own')
        group by vu.relation_role
    loop
        if row.rrole = 'vwr' then vac_viewer_list = row.mails; end if;
        if row.rrole = 'own' then vac_owner_list = row.mails; end if;
    end loop;
end;
$$ language plpgsql;

