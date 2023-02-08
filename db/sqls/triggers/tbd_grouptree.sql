drop trigger if exists tbd_grouptree on grouptree;
create trigger tbd_grouptree
    before delete
    on grouptree
    for each row
execute procedure grouptree_tbd();

