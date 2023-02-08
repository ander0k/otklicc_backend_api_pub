create table tcdbinfo(
	name text not null constraint tcdbinfo_pkey primary key,
	mask text,
	value text,
	tag integer default 0 not null
);

