drop trigger if exists tbi_grouptree on grouptree;
create trigger tbi_grouptree
    before insert
    on grouptree
    for each row
execute procedure grouptree_tbi();

