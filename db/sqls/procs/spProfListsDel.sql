drop function if exists spProfListsDel;
create function spProfListsDel(
     _user_id uuid
    ,_complist text
    ,_ownlist text
    ,_vwrlist text
) returns void
as $$
begin
    if _complist is not null then
        perform spProfCompDel(_user_id, _complist);
    end if;
    if coalesce (_ownlist, _vwrlist) is not null then
        perform spProfVcnDel(_user_id, _ownlist, _vwrlist);
    end if;
end;
$$ language plpgsql;