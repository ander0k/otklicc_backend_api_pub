create table vcn_terms(
    id        uuid default gen_random_uuid() not null primary key,
    vcn_id    uuid not null constraint vcn_terms_vcn_fk
                            references vacancy on delete cascade,
    ord       smallint default 0 not null,
    description text,
    created timestampz default CURRENT_TIMESTAMP not null
);
comment on table vcn_terms is 'Плюшки вакансий"';
