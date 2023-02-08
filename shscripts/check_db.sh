#!/usr/bin/env bash

echo "ping db.otkli.cc..."
if ping -c 1 db.otkli.cc &> /dev/null
then
  echo "...ping db.otkli.cc ok."
else
  echo "...ping failed, db.otkli.cc host is down!"
fi

echo "ping 18.198.224.115..."
if ping -c 1 18.198.224.115 &> /dev/null
then
  echo "...ping 18.198.224.115 ok."
else
  echo "...ping failed, 18.198.224.115 host is down!"
fi

# sudo apt install postgresql-client-common
# sudo apt install postgresql-client
# Утилита pg_isready возвращает в оболочку 0, если сервер принимает подключения,
# 1, если он сбрасывает подключения (например, во время загрузки),
# 2, если при попытке подключения не получен ответ,
# 3, если попытки подключения не было

export PGCONNECT_TIMEOUT=3

echo "check pg_isready by ip 18.198.224.115..."
pg_isready -h 18.198.224.115 -p 5432 -d db_otklicc -U api.otkli.cc
echo "run sql query on postgres addressing by ip: 18.198.224.115"
echo '\x \\ SELECT datname,  usename,  application_name, client_addr, client_hostname, backend_start, query_start, wait_event_type, wait_event, state, query,  backend_type, ssl from pg_stat_activity as pgact left join pg_stat_ssl pss on pgact.pid = pss.pid WHERE length(datname)>0 order by pgact.pid, pgact.backend_start;' | psql -h 18.198.224.115 -p 5432 -d db_otklicc -U api.otkli.cc



echo "check pg_isready by hostname db.otkli.cc..."
pg_isready -h db.otkli.cc -p 5432 -d db_otklicc -U api.otkli.cc
echo "run sql query on postgres addressing by hostname db.otkli.cc:"
echo '\x \\ SELECT datname,  usename,  application_name, client_addr, client_hostname, backend_start, query_start, wait_event_type, wait_event, state, query,  backend_type, ssl from pg_stat_activity as pgact left join pg_stat_ssl pss on pgact.pid = pss.pid WHERE length(datname)>0 order by pgact.pid, pgact.backend_start;' | psql -h db.otkli.cc -p 5432 -d db_otklicc -U api.otkli.cc
