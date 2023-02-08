drop function if exists v_vac_deads_tu;
create or replace function v_vac_deads_tu() returns trigger
    language plpgsql
as
$$
declare _status int;
begin
    _status = new.status;
    if new.mail_sended = 2 then
        _status = 50;
    end if;
    update vacancy set mail_sended = new.mail_sended, status = _status
    where id = new.vac_id;
    return NEW;
end;
$$;

