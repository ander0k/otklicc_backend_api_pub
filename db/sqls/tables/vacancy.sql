create table vacancy(
     id          uuid       default gen_random_uuid() not null primary key
    ,title       text
    ,code        text       default gen_short_code() not null
    ,experience  smallint   default 10 not null
    ,post_date   timestamp
    ,leave_days  int        default 30 not null
    ,deadline    date       not null generated always as (coalesce(post_date::date,created::date) + leave_days) stored
    ,mail_sended smallint   default  0 not null
    ,busyness    smallint   default  0 not null
    ,view_count  integer    default  0 not null
    ,status      smallint   default 10 not null
    ,salary_lo   integer
    ,salary_hi   integer
    ,currency    varchar(3) default 'RUB'::character varying not null
    ,term        smallint   default 10 not null
    ,about       text
    ,status_time timestamp
    ,company_id  uuid not null constraint vacancy_comp_fk
                               references company on delete cascade
    ,created     timestamp default CURRENT_TIMESTAMP not null
    ,updated     timestamp default CURRENT_TIMESTAMP not null
    ,deleted     timestamp
    ,last_db_user text default CURRENT_USER not null
    ,last_app_user_id uuid
);
create index vacancy_dead_ndx on vacancy (deadline desc);

comment on column vacancy.mail_sended is '
флаг "письмо отправлено":
  1 - за 3 дня до дедлайна (HR-у)
  2 - в дедлайн (фидбеки (не)отскоренным CUS и "вакансия ушла в архив" HR-у)
';

