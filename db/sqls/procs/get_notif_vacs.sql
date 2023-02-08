drop function if exists get_notif_vacs;
create or replace function get_notif_vacs(u_id uuid)
returns TABLE(
      link_id uuid
     ,vac_code text
     ,vac_title text
     ,com_code text
     ,com_name text
     ,com_img text
)
as $$
begin
    for link_id,vac_code,vac_title,com_code,com_name,com_img in
        select vc.id, v.code,v.title,c.code,c.name,c.logo_image
        from v_vcn_cus vc
        join vacancy v on v.id = vc.vacancy_id
        join company c on c.id = v.company_id
        where vc.user_id = u_id
          and vc.cus_status = 10
          and vc.mail_sended is null
    loop
        return next;
    end loop;
end;
$$ language plpgsql;

