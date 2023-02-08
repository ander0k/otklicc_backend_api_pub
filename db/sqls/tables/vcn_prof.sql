drop table if exists vcn_prof;
create table vcn_prof(
     id uuid default gen_random_uuid() not null primary key
    ,prof_id uuid not null constraint vcn_prof_prof_id_fk
                           references professions on delete cascade
    ,vacancy_id  uuid not null constraint vcn_prof_vcn_id_fk
                           references vacancy on delete cascade
);
create unique index vcn_prof_unq
    on vcn_prof(prof_id, vacancy_id);

comment on table vcn_prof is 'Профессии у вакансии';


