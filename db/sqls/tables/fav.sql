drop table if exists fav;
create table fav(
    id uuid default gen_random_uuid() not null primary key,
    owner uuid not null constraint fav_owner_fk references app_user on delete cascade,
    apply_time timestamptz,
    name text not null,
    professions text,
    parent_professions text,
    company text,
    parent_company text,
    geos text,
    parent_geos text,
    experience text,
    deadline bool,
    popular bool
);
create unique index fav_name_uindex on fav(name);
create index fav_apply_time_ndx on fav (apply_time desc);

comment on table fav is 'Параметры поиска для "Search" endpoint';

