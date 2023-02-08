drop function if exists spVacancyNew;
create or replace function spVacancyNew(
     _company_id uuid
    ,_title text
    ,_status int
    ,_experience int
    ,_leave_days int
    ,_busyness int
    ,_professions text
    ,_geos text
    ,_salary_lo int
    ,_salary_hi int
    ,_currency varchar(3)
    ,_term int
    ,_about text
    ,_demands json
    ,_terms json
    ,_vac_owner_list text
    ,_vac_viewer_list text
--
   ,out code text
   ,out title text
   ,out viewers text
   ,out owners text
)
as $$
    declare _id uuid;
begin
    if _professions is null then
        raise EXCEPTION 'professions cannot be null';
    end if;
    if _geos is null then
        raise EXCEPTION 'geos cannot be null';
    end if;

    insert into vacancy(
             title, experience, leave_days, busyness, status, salary_lo, salary_hi, currency, term, about, company_id
    )values(_title,_experience,_leave_days,_busyness,_status,_salary_lo,_salary_hi,_currency,_term,_about,_company_id)
    returning id into _id;
    -- добавить профессии
    call _spMakeProfList(_id, _professions);
    -- добавить geo
    call _spMakeGeoList(_id, _geos);

    insert into vcn_demand(vacancy_id,ord,wording)
    select _id,row_number() OVER() as ord,value
    from json_array_elements_text(_demands);

    insert into vcn_terms(vcn_id,ord,description)
    select _id,row_number() OVER() as ord,value
    from json_array_elements_text(_terms);
----
    select into code, title
        v.code, v.title from vacancy v where v.id = _id;

    select into viewers
        string_agg(mail, ',') from _spMakeVcnList(_id, false, _vac_viewer_list);

    select into owners
        string_agg(mail, ',') from _spMakeVcnList(_id, true, _vac_owner_list);

end;
$$ language plpgsql;
comment on function spVacancyNew is
'Метод POST вакансии; возвращает info: json(code,title) созданной вакансии и перечни email (csv), свежедобавленных в vcn_user';

