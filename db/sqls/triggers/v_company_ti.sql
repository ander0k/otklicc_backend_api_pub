drop function if exists v_company_ti;
create or replace function v_company_ti() returns trigger
    language plpgsql
as
$$
begin
    if new.owner_user_id is null and new.owner_email is not null then
        select id into new.owner_user_id from app_user where email = new.owner_email;
    end if;
    for i in 1..3 by 1 loop
        new.code = gen_short_code();
        exit when not exists(select 1 from company where code = new.code);
    end loop;
    insert into company(name,verified,code,color,sec_color,about,logo_image,owner_user_id,status,thumbnail_image,sub_name,synonyms)
    values(new.name,new.verified,new.code,new.color,new.sec_color,new.about,new.logo_image,new.owner_user_id,
           new.status,new.thumbnail_image,new.sub_name,new.synonyms
    ) returning id into new.id;

    if new.owner_user_id is not null then
        insert into prof_company(user_id, company_id) values(new.owner_user_id, new.id)
        on conflict do nothing;
    end if;

    return NEW;
end;
$$;
