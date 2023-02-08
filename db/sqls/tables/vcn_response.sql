drop table if exists vcn_response;
create table vcn_response(
    id                uuid default gen_random_uuid() not null primary key,
    is_draft          bool not null default false,
    content           text not null,
    user_id           uuid not null constraint vcn_response_usr_fk references app_user on delete cascade,
    demand_id         uuid not null constraint vcn_response_dmd_fk references vcn_demand on delete cascade,
    grade             integer,
    grader_id         uuid constraint vcn_response_scor_fk references app_user on delete set null,
    grade_time        timestamp with time zone,
    hidden 	          bool default false not null,
    created           timestamp with time zone not null default CURRENT_TIMESTAMP,
    updated           timestamp with time zone default CURRENT_TIMESTAMP,
    deleted           timestamp with time zone,
    last_db_user      text default CURRENT_USER not null,
    last_app_user_id  uuid
);
create unique index vcn_response_unq_index
	on vcn_response (user_id, demand_id, is_draft);

comment on table vcn_response is 'отклики на требования вакансии';
comment on column vcn_response.demand_id is 'связь с требованием';
comment on column vcn_response.user_id is 'чей отклик';
comment on column vcn_response.content is 'содержимое отклика';
comment on column vcn_response.grade_time is 'когда установлена оценка';
comment on column vcn_response.grade is 'оценка';
comment on column vcn_response.grader_id is 'кто поставил оценку';
comment on column vcn_response.created is 'отметка времени создания записи';
comment on column vcn_response.updated is 'отметка времени изменения записи';
comment on column vcn_response.deleted is 'признак и отметка времени удаления записи, запись считается удалённой, если значение этого поля отлично от NULL';
comment on column vcn_response.last_db_user is 'имя пользователя базы данных, внесшего последнее изменение записи';
comment on column vcn_response.last_app_user_id is 'ссылка на пользователя otklicc, последним изменившего запись';
