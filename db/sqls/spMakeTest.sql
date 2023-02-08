drop procedure if exists spMakeTest;
create or replace procedure spMakeTest(CleanOnly int default 0)
as $$
begin
    if CleanOnly then
        delete from company;
        delete from app_user;
        insert into app_user(is_active,code,id,utype,email,last_name,first_name,passkey) values
          (true,'adm','2fef6c8a-b746-4494-8727-4a2bee1e8dd8','ADM','adm@otkli.cc',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
         ,(true,'666','ad3029ae-a18a-419a-b769-8bbffbf338ce','ADM','sl.minimus@gmail.com','Вий','Хрон Монадович','$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
         ,(true,'homa','82c047db-38c7-457b-8e10-601a30387827','CUS','homa.brute@bk.ru','Хома','Брут','$2b$12$/Frq98jZccWZ8pZOmZTF6umnxieaQ6v6z4f.Tpz8sdky7/kMk3syi')
         ,(true,'slhr','96779a5e-8312-460c-afa4-9b0522dc3d67','HR','sl_minimus@mail.ru',null,null,'$2b$12$JOmcM3qZzmq7DO7sp0cJK.j1EXXxXkv5AjB2gzfPUPJ/rOAqAkAv.')
        ;
        delete from geos;
        delete from professions;
        delete from dmn_metatag;
        delete from fav;
        delete from grouptree where id_own is not null;
        delete from prof_company;
        return;
    end if;
    -------------------------------------------------
     delete from geos;
    delete from professions;
    delete from dmn_metatag;
    -------------------------------------------------
    delete from company where id = '7f47eb72-250e-40ae-b427-430ae1a73360';
    delete from company where id = '3648e5d4-4b59-4db4-9194-9ab49c892387';
    delete from company where id = '25b519fb-6705-4c67-b34c-0fb4078d2e04';
    delete from company where id = '954317f3-3e3a-40d5-89d5-6a221e898f4c';
    delete from company where id = 'ff37fc08-bb90-40e7-af26-bebc86318807';
    delete from company where id = 'e643b4aa-69d7-4231-b7a1-1f82c9ae2723';
    -------------------------------------------------
    delete from app_user where email = 'sl.minimus@gmail.com';
    delete from app_user where email = 'ander@nist.ru';
    delete from app_user where email = 'hr@nist.ru';
    delete from app_user where email = 'inbox@otkli.cc';
    delete from app_user where email = 'adm@otkli.cc';
    delete from app_user where email = 'tri6odin@gmail.com';
    delete from app_user where email = 'cus@otkli.cc';
    delete from app_user where email = 'ilobzer@gmail.com';
    delete from app_user where email = 'hr@otkli.cc';
    -------------------------------------------------
    delete from vacancy where code = 'ManYan';
    delete from vacancy where code = 'GruZber';
    delete from vacancy where code = '5kaToVed';
    delete from vacancy where code = 'RNBroker';
    delete from vacancy where code = 'vac';
    delete from vacancy where code = 'vac2';
    -------------------------------------------------
    --********************************************************
    insert into app_user(is_active,code,id,utype,email,last_name,first_name,passkey) values
         (true,'16','6d304ada-577a-4e63-825c-1ad789751322','CUS','ander@nist.ru',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
        ,(true,'hhr','e53a9597-eedd-44df-b8d6-75071d28c6b8','HR','hr@nist.ru',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
        ,(true,'666','ad3029ae-a18a-419a-b769-8bbffbf338ce','ADM','sl.minimus@gmail.com','Вий','Хрон Монадович','$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')

        ,(true,'inbox','3cf6e306-1d0c-4640-8747-9167563cbeea','ADM','inbox@otkli.cc',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
        ,(true,'adm','2fef6c8a-b746-4494-8727-4a2bee1e8dd8','ADM','adm@otkli.cc',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
        ,(true,'tri6odin','12cb1d76-f905-407d-b9a4-913a1956d3ce','CUS','tri6odin@gmail.com',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
        ,(true,'cus','df19709f-fb7c-45cf-8ad9-447eb4edea2e','CUS','cus@otkli.cc',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
        ,(true,'ilobzer','d75d6234-b017-4b6f-a34c-75df239e2b0b','HR','ilobzer@gmail.com',null,null,'$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
        ,(true,'hr','278d2110-d29e-4344-b4df-99822370f958','HR','hr@otkli.cc','Windows','M.S.','$2b$12$/Ic4RTUza2G2E2HCNTSZ7e0BOUesCFNoYsLxbHeWfpp8Z/EKzVhtK')
    ;
    -------------------------------------------------
    insert into company(id,status,code,name,owner_user_id) values
         ('7f47eb72-250e-40ae-b427-430ae1a73360',40,'5-ka','Пятерочка','e53a9597-eedd-44df-b8d6-75071d28c6b8')
        ,('3648e5d4-4b59-4db4-9194-9ab49c892387',40,'sber','Сбербанк','d75d6234-b017-4b6f-a34c-75df239e2b0b')
        ,('25b519fb-6705-4c67-b34c-0fb4078d2e04',40,'yandex','Яндекс','278d2110-d29e-4344-b4df-99822370f958')
        ,('954317f3-3e3a-40d5-89d5-6a221e898f4c',40,'RN','РосНефть','e53a9597-eedd-44df-b8d6-75071d28c6b8')
        ,('ff37fc08-bb90-40e7-af26-bebc86318807',40,'comp','company','278d2110-d29e-4344-b4df-99822370f958')
        ,('e643b4aa-69d7-4231-b7a1-1f82c9ae2723',40,'comp2','company2','d75d6234-b017-4b6f-a34c-75df239e2b0b')
    ;
    -------------------------------------------------
    insert into vacancy(id,company_id,code,title) values
         ('8dc2eab4-d51e-4de0-a8e6-f5dcdcbb1558','25b519fb-6705-4c67-b34c-0fb4078d2e04','ManYan','МЕНЕДЖЕР В Яндекс')
        ,('a59bfd5f-fa00-46c0-9dd5-5304470c902b','3648e5d4-4b59-4db4-9194-9ab49c892387','GruZber','ГРУЗЧИК В Сбербанк')
        ,('1ee2e4f3-f0f9-473a-9925-cdd1e8cad1fc','7f47eb72-250e-40ae-b427-430ae1a73360','5kaToVed','Пятерочка товаровед')
        ,('ce1f0fec-0db7-4474-b859-d6f53e675f99','954317f3-3e3a-40d5-89d5-6a221e898f4c','RNBroker','РосНефть брокер')
        ,('ccc4d0c9-7238-45ba-8ce3-2fbb3af7fcc3','ff37fc08-bb90-40e7-af26-bebc86318807','vac','vacancy')
        ,('bc038b3e-8b41-4bc3-ac61-23edeac419ad','e643b4aa-69d7-4231-b7a1-1f82c9ae2723','vac2','vacancy2')
    ;
    --********************************************************
    ----------------------------------------------------------
    insert into prof_company(user_id, company_id) values
         ((select id from app_user where code = 'inbox'),   (select id from company where code = 'comp'))
        ,((select id from app_user where code = 'inbox'),   (select id from company where code = 'comp2'))
        ,((select id from app_user where code = 'adm'),     (select id from company where code = 'comp'))
        ,((select id from app_user where code = 'adm'),     (select id from company where code = 'comp2'))
        ,((select id from app_user where code = 'tri6odin'),(select id from company where code = 'comp'))
        ,((select id from app_user where code = 'tri6odin'),(select id from company where code = 'comp2'))
        ,((select id from app_user where code = 'cus'),     (select id from company where code = 'comp'))
        ,((select id from app_user where code = 'cus'),     (select id from company where code = 'comp2'))
        ,((select id from app_user where code = 'ilobzer'), (select id from company where code = 'comp'))
        ,((select id from app_user where code = 'hr'),      (select id from company where code = 'comp2'))
        ,((select id from app_user where code = 'hr'),      (select id from company where code = 'sber'))
    ;
    ----------------------------------------------------------------------
    insert into vcn_user(relation_role,user_id,vacancy_id) values
         ('vwr','2fef6c8a-b746-4494-8727-4a2bee1e8dd8', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b')
        ,('vwr','12cb1d76-f905-407d-b9a4-913a1956d3ce', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b')
        ,('own','278d2110-d29e-4344-b4df-99822370f958', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b')
        ,('vwr','278d2110-d29e-4344-b4df-99822370f958', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b')
        ,('vwr','df19709f-fb7c-45cf-8ad9-447eb4edea2e', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b')
        ,('vwr','d75d6234-b017-4b6f-a34c-75df239e2b0b', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b')
        ,('vwr','3cf6e306-1d0c-4640-8747-9167563cbeea', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b'),

         ('vwr',(select id from app_user where code = 'inbox'),     (select id from vacancy where code = 'vac'))
        ,('vwr',(select id from app_user where code = 'inbox'),     (select id from vacancy where code = 'vac2'))
        ,('vwr',(select id from app_user where code = 'adm'),       (select id from vacancy where code = 'vac'))
        ,('vwr',(select id from app_user where code = 'adm'),       (select id from vacancy where code = 'vac2'))
        ,('vwr',(select id from app_user where code = 'tri6odin'),  (select id from vacancy where code = 'vac'))
        ,('vwr',(select id from app_user where code = 'tri6odin'),  (select id from vacancy where code = 'vac2'))
        ,('vwr',(select id from app_user where code = 'cus'),       (select id from vacancy where code = 'vac'))
        ,('vwr',(select id from app_user where code = 'cus'),       (select id from vacancy where code = 'vac2'))
        ,('vwr',(select id from app_user where code = 'ilobzer'),   (select id from vacancy where code = 'vac'))
        ,('vwr',(select id from app_user where code = 'ilobzer'),   (select id from vacancy where code = 'vac2'))
        ,('vwr',(select id from app_user where code = 'hr'),        (select id from vacancy where code = 'vac'))
        ,('vwr',(select id from app_user where code = 'hr'),        (select id from vacancy where code = 'vac2'))
    ;
    ----------------------------------------------------------------------
    insert into cus_to_vac(id, user_id, vcn_id) values -- cus@otkli.cc <-> GruZber
         ('33b0a562-e689-4a5a-ab8f-425178bd391c','df19709f-fb7c-45cf-8ad9-447eb4edea2e','a59bfd5f-fa00-46c0-9dd5-5304470c902b')
    ;
    ----------------------------------------------------------------------
    insert into vcn_demand(id, vacancy_id, ord, wording, weight) values
         ('7dde82f3-b9da-4d69-9197-3f2b1120362c', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b', 1, 'ЦПШ + ВПШ', 1)
        ,('f04fd7c6-c1b7-4eab-908f-7949f102ac73', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b', 0, 'Отвращение к деньгам', 55)
        ,('5f4f2250-4569-4c36-a958-8450a41ec86f', '8dc2eab4-d51e-4de0-a8e6-f5dcdcbb1558', 0, 'Права категории B,C', 1)
        ,('2054520d-e209-457c-af78-c5fb98624434', '8dc2eab4-d51e-4de0-a8e6-f5dcdcbb1558', 1, 'Умение водить самолет', 3)
        ,('91cc7e20-2b56-45b4-a0ba-12785c7939f8', '8dc2eab4-d51e-4de0-a8e6-f5dcdcbb1558', 2, 'Знание Москвы, включая переулки', 11)
    ;
    ----------------------------------------------------------------------
    insert into vcn_response(id, user_id, demand_id, content) values
         ('e06a8a8b-6648-4416-948f-c1691f884457', 'df19709f-fb7c-45cf-8ad9-447eb4edea2e', '7dde82f3-b9da-4d69-9197-3f2b1120362c', 'и курсы молодых доярок')
        ,('9d94aa7c-a092-4444-a2d8-1fc71648defd', 'df19709f-fb7c-45cf-8ad9-447eb4edea2e', 'f04fd7c6-c1b7-4eab-908f-7949f102ac73', 'дажи кюшить нэ магу!')
    ;
    ----------------------------------------------------------------------
    insert into vcn_terms (id, vcn_id, description) values
         ('600e93a8-8285-4821-9c3c-edeb95adcc4e', 'ce1f0fec-0db7-4474-b859-d6f53e675f99', 'Детский сад')
        ,('b75c50b8-e2c0-4a9c-a0c5-8f7ac6b649c9', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b', 'Парковка')
        ,('336e6de9-eb88-4db1-be0c-391c0ff0723f', 'a59bfd5f-fa00-46c0-9dd5-5304470c902b', 'Спортзал с блэкджеком и...')
        ,('b95c768f-e4c0-4da9-bed8-c6a4649c797f', '8dc2eab4-d51e-4de0-a8e6-f5dcdcbb1558', 'Медстраховка')
        ,('b03357ba-d0bc-4302-bbd3-26706e837c28', '8dc2eab4-d51e-4de0-a8e6-f5dcdcbb1558', 'Соцпакет')
        ,('21431f0a-e714-442c-9235-8243da94c32e', 'ce1f0fec-0db7-4474-b859-d6f53e675f99', 'Квартальная премия')
        ,('bf26a413-6fa1-4830-af29-a6cb358579fd', '8dc2eab4-d51e-4de0-a8e6-f5dcdcbb1558', 'Зарубежные командировки (Украина, Уазахстан)')
    ;
    ----------------------------------------------------------------------
end;
$$ language plpgsql;
