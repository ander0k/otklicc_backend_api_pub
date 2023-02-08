drop table if exists cus_to_vac;
create table cus_to_vac(
     id uuid  default gen_random_uuid() not null primary key
    ,status   smallint not null default 0
    ,user_id  uuid not null constraint ctv_user_fk
                           references app_user on delete cascade
    ,vcn_id   uuid not null constraint cnv_vcn_fk
                           references vacancy on delete cascade
    ,favored  timestamp with time zone default CURRENT_TIMESTAMP
    ,visited  timestamp with time zone default CURRENT_TIMESTAMP not null
);

comment on table cus_to_vac is
    'пользовательский список просмотренных/отмеченных вакансий';