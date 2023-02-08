drop  table if exists vcn_user;
create table vcn_user(
     id uuid default gen_random_uuid() not null primary key
    ,user_id uuid not null constraint vcn_user_user_id_fk
                           references app_user on delete cascade
    ,vacancy_id  uuid not null constraint vcn_user_vcn_id_fk
                           references vacancy on delete cascade
    ,relation_role text not null
    ,cus_status int default 0 not null
    ,mail_sended date
);
create index vcn_user_mail_ndx on vcn_user (mail_sended desc);
create index vcn_user_stat_ndx on vcn_user (cus_status);

create unique index vcn_user_unq
    on vcn_user (user_id, vacancy_id, relation_role);

comment on table vcn_user is
'Связи и отношения между пользователями и вакансиями
relation_role: own|vwr|cus;
own: contained in vac_viewer_list;
vwr: contained in vac_owner_list;
cus: for cus_status
';



