drop table if exists professions;
create table professions(
	id uuid default gen_random_uuid() not null primary key,
	name text not null,
        synonyms text,
	verified boolean default false,
	code text,  -- код по классификатору
	node_id uuid default '00000000-0000-0000-0000-000000000001'::uuid not null
                     constraint prof_node_fk references grouptree on delete cascade,
	created timestamp with time zone default CURRENT_TIMESTAMP not null,
	updated timestamp with time zone default CURRENT_TIMESTAMP,
	deleted timestamp with time zone,
	last_db_user text default CURRENT_USER
);
create unique index professions_name_uindex on professions(lower(name));
comment on table professions is 'справочник профессий';
comment on column professions.verified is 'верифицировано модератором';
comment on column professions.name is 'наименование профессии';
comment on column professions.code is 'ссылка на узел классификатора';
