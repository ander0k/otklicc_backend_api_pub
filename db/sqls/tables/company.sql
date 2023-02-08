create table company
(
	id uuid default gen_random_uuid() not null primary key,
	name text not null,
	status int default 10 not null,
	verified boolean default false,
	code text default gen_short_code() not null,
	color text,
	sec_color text,
	logo_image text,
	thumbnail_image text,
	about text,
	sub_name text,
	synonyms text,
	owner_user_id uuid constraint company_own_fk references app_user,
	created timestamp with time zone default CURRENT_TIMESTAMP not null,
	updated timestamp with time zone default CURRENT_TIMESTAMP,
	deleted timestamp with time zone,
	last_db_user text default CURRENT_USER,
	last_app_user_id uuid
);

create unique index ix_company_code on company(code);
create index company_name_ndx on company(lower(name));
create index company_subname_ndx on company(lower(sub_name));


comment on table company is 'компании, организации';
comment on column company.id is 'внутренний (скрытый) уникальный идентификатор записи';
comment on column company.name is 'название компании';
comment on column company.verified is 'верифицировано модератором';
comment on column company.code is 'публичный (постоянный) уникальный идентификатор записи и название для использования в ссылках (url) или именах объектов и элементов (записывается печатными символами из первой половины таблицы ASCII)';
comment on column company.color is 'фирменный цвет HTML Color Codes hex (#00FFFF for Aqua)';
comment on column company.sec_color is 'второй фирменный цвет HTML Color Codes hex (#00FFFF for Aqua)';
comment on column company.logo_image is 'ссылка (hash) на картинку';
comment on column company.about is 'описание, дополнительные сведения';
comment on column company.created is '[дата и] время создания записи';
comment on column company.updated is '[дата и] время изменения записи';
comment on column company.deleted is 'признак и [дата и] время удаления записи, запись считается удалённой, если значение этого поля отлично от NULL';
comment on column company.last_db_user is 'имя пользователя базы данных, внесшего последнее изменение записи';
comment on column company.last_app_user_id is 'ссылка на пользователя otklicc, последним изменившего запись';
comment on column company.owner_user_id is 'ссылка на владельца записи';
