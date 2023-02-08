create table app_user(
	id uuid default gen_random_uuid() not null primary key,
	utype text default 'CUS'::text not null,
	email text not null,
	is_active boolean default true not null,
	code text default gen_short_code() not null,
	last_name text,
	first_name text,
	prof_view integer default 20 not null,
	reqr_view boolean default true not null,
	comp_view boolean default true not null,
	phone text,
	about text,
	img text,
	notifications integer default 10 not null,
	educations text,
	jobs text,
	actual_start timestamp default CURRENT_TIMESTAMP not null,
	actual_end timestamp,
	created timestamp default CURRENT_TIMESTAMP not null,
	updated timestamp default CURRENT_TIMESTAMP,
	deleted timestamp,
	last_db_user text default CURRENT_USER not null,
	last_app_user_id uuid,
	passkey text,
	company_id uuid
);

create unique index ix_app_user_email
	on app_user (email);

create unique index ix_app_user_code
	on app_user (code);
