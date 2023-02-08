create table prof_company(
	id uuid default gen_random_uuid() not null primary key,
	user_id uuid not null constraint prof_comp_user_fk references app_user on delete cascade,
	company_id uuid not null constraint prof_comp_comp_fk references company on delete cascade,
	created timestamp default CURRENT_TIMESTAMP not null,
	deleted timestamp,
	last_db_user text default CURRENT_USER not null,
	last_app_user_id uuid,
        constraint prof_company_unq unique (user_id, company_id)
);

comment on table prof_company is 'связь компаний и профилей (app_user)';

