drop table if exists vcn_geo;
create table vcn_geo(
     id uuid default gen_random_uuid() not null primary key
    ,geo_id uuid not null constraint vcn_geo_geo_id_fk
                          references geos on delete cascade
    ,vacancy_id  uuid not null constraint vcn_geo_vcn_id_fk
                          references vacancy on delete cascade
);
create unique index vcn_geo_unq
    on vcn_geo(geo_id, vacancy_id);

comment on table vcn_geo is 'Локации у вакансии';


