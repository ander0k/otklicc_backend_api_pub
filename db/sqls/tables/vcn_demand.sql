drop table if exists vcn_demand;
create table vcn_demand(
    id            uuid default gen_random_uuid() not null primary key,
    vacancy_id    uuid not null constraint vcn_demand_vac_fk
                                references vacancy on delete cascade,
    ord           smallint default 0 not null,
    wording       text not null,
    weight        real default 1.0 not null,
    metatag       text constraint vcn_demand_metatag_fkey
                  references dmn_metatag on delete set null,
    coefficient   int default 50 not null,
    created       timestamp with time zone default CURRENT_TIMESTAMP not null,
    updated       timestamp with time zone default CURRENT_TIMESTAMP,
    deleted       timestamp with time zone,
    last_db_user  text default CURRENT_USER not null,
    last_app_user uuid
);

comment on table vcn_demand is 'требования из вакансий';
comment on column vcn_demand.id is 'внутренний (скрытый) уникальный идентификатор записи';
comment on column vcn_demand.vacancy_id is 'ссылка на вакансию';
comment on column vcn_demand.ord is 'номер требования (по порядку)';
comment on column vcn_demand.wording is 'формулировка требования';
comment on column vcn_demand.weight is 'ценность, рейтинг, коэффициент, вес, значимость';
comment on column vcn_demand.created is 'отметка времени создания записи';
comment on column vcn_demand.updated is 'отметка времени изменения записи';
comment on column vcn_demand.deleted is 'признак и отметка времени удаления записи, запись считается удалённой, если значение этого поля отлично от NULL';
comment on column vcn_demand.last_db_user is 'имя пользователя базы данных, внесшего последнее изменение записи';
comment on column vcn_demand.last_app_user is 'ссылка на пользователя otklicc, последним изменившего запись';
