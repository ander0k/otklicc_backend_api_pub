drop function if exists spVacancyUpd;
create or replace function spVacancyUpd(
     _id uuid
    ,_title text
    ,_professions text
    ,_status int
    ,_experience int
    ,_leave_days int
    ,_busyness int
    ,_geos text
    ,_salary_lo int
    ,_salary_hi int
    ,_currency varchar(3)
    ,_term int
    ,_about text
    ,_vac_owner_list text
    ,_vac_viewer_list text
---
    ,out viewers text
    ,out owners text
)
as $$
    declare _prof_id uuid;
begin
    _prof_id = null;
    if coalesce(_professions,'') <> '' then
        call _spMakeProfList(_id, _professions);
    end if;
    if coalesce(_geos,'') <> '' then
        call _spMakeGeoList(_id, _geos);
    end if;

    update vacancy set
         title          = coalesce(_title      , title         )
        ,status         = coalesce(_status     , status        )
        ,experience     = coalesce(_experience , experience    )
        ,leave_days     = coalesce(_leave_days , leave_days    )
        ,busyness       = coalesce(_busyness   , busyness      )
        ,salary_lo      = coalesce(_salary_lo  , salary_lo     )
        ,salary_hi      = coalesce(_salary_hi  , salary_hi     )
        ,currency       = coalesce(_currency   , currency      )
        ,term           = coalesce(_term       , term          )
        ,about          = coalesce(_about      , about         )
    where id = _id;

    select into viewers
        string_agg(mail, ',') from _spMakeVcnList(_id, false, _vac_viewer_list);

    select into owners
        string_agg(mail, ',') from _spMakeVcnList(_id, true, _vac_owner_list);
end;
$$ language plpgsql;
