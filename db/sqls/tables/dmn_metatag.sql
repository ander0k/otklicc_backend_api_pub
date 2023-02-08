drop table if exists dmn_metatag;
create table dmn_metatag
(
    name     text not null primary key,
    synonyms text,
    node_id  uuid default '00000000-0000-0000-0000-000000000003'::uuid not null
        constraint geo_node_fk references grouptree on delete set default
);
comment on table dmn_metatag is 'метатэги к требованиям вакансий';
comment on column dmn_metatag.name is
    'текстовое значение метатега (краткая запись сути требования)';
