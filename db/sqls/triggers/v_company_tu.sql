drop function if exists v_company_tu;
create or replace function v_company_tu() returns trigger
    language plpgsql
as
$$
begin
    if new.owner_email is not null then
        select id into new.owner_user_id from app_user where email = new.owner_email;
    end if;
    update company set
        name            = coalesce(new.name           ,  old.name           ),
        status          = coalesce(new.status         ,  old.status         ),
        verified        = coalesce(new.verified       ,  old.verified       ),
        code            = coalesce(new.code           ,  old.code           ),
        color           = coalesce(new.color          ,  old.color          ),
        sec_color       = coalesce(new.sec_color      ,  old.sec_color      ),
        logo_image      = coalesce(new.logo_image     ,  old.logo_image     ),
        thumbnail_image = coalesce(new.thumbnail_image,  old.thumbnail_image),
        about           = coalesce(new.about          ,  old.about          ),
        sub_name        = coalesce(new.sub_name       ,  old.sub_name       ),
        synonyms        = coalesce(new.synonyms       ,  old.synonyms       ),
        owner_user_id   = coalesce(new.owner_user_id  ,  old.owner_user_id  )
    where id = new.id;

    select * into NEW from v_company v where v.id = new.id;
    return NEW;
end;
$$;

