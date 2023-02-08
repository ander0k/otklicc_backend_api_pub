drop table if exists grouptree;
create table grouptree(
   id uuid default gen_random_uuid() not null primary key
  ,id_own uuid default null constraint grouptree_own_fk references grouptree on delete cascade
  ,grp_class int not null
  ,name text not null
  ,code text  -- код по классификатору
  ,syn text
  ,checked bool not null default false
  ,created timestamp with time zone default CURRENT_TIMESTAMP not null
  ,updated timestamp with time zone default CURRENT_TIMESTAMP
  ,deleted timestamp with time zone
  ,last_db_user text default CURRENT_USER
);
create unique index grouptree_unq on grouptree(grp_class,lower(name));

comment on table grouptree is 'классификатор (профессии, гео...)';
comment on column grouptree.checked is 'True: создано автоматически, требует внимания администратора (назначить правильный owner)';
comment on column grouptree.grp_class is '[1,2,3]: профессии, гео, тэг)';

insert into grouptree(id, id_own, grp_class, name, code) values
 ('00000000-0000-0000-0000-000000000001',null,1,'Прочие профессии','--')
,('00000000-0000-0000-0000-000000000002',null,2,'Прочие локации','--')
,('00000000-0000-0000-0000-000000000003',null,3,'Прочие тэги','--')
;
