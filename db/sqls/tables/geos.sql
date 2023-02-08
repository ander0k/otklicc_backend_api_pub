drop table if exists geos;
create table geos(
	id uuid default gen_random_uuid() not null primary key,
	name text not null,
        synonyms text,
	verified boolean default false,
	code text,  -- код по классификатору
	node_id uuid default '00000000-0000-0000-0000-000000000002'::uuid not null
                     constraint geo_node_fk references grouptree on delete cascade,
	created timestamp with time zone default CURRENT_TIMESTAMP not null,
	updated timestamp with time zone default CURRENT_TIMESTAMP,
	deleted timestamp with time zone,
	last_db_user text default CURRENT_USER
);
create unique index geo_name_uindex on geos(lower(name));
comment on table geos is 'справочник локаций';
comment on column geos.verified is 'верифицировано модератором';
comment on column geos.name is 'наименование';
comment on column geos.code is 'ссылка на узел классификатора';
