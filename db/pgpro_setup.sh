#!/usr/bin/env bash
# комманды установки и конфигурации сервера БД

sudo locale-gen ru_RU

sudo locale-gen ru_RU.UTF-8

sudo update-locale LANG="ru_RU.UTF-8"

sudo update-locale LC_MESSAGES="en_US.UTF-8"

sudo timedatectl set-timezone Europe/Moscow

curl -o pgpro-repo-add.sh https://repo.postgrespro.ru/pgpro-14/keys/pgpro-repo-add.sh

sh pgpro-repo-add.sh

# минимальный набор пакетов для установки:
sudo apt install postgrespro-std-14-client postgrespro-std-14-libs postgrespro-std-14-server  postgrespro-std-14-contrib

# расширенный набор пакетов
# sudo apt install postgrespro-std-14-client postgrespro-std-14-libs postgrespro-std-14-server postgrespro-std-14-contrib mamonsu pg-probackup-std-14 pgpro-controldata pgpro-pwr-std-14 pgpro-stats-std-14 pg-probackup-std-14 pgbouncer pgpro-pwr-std-14

sudo apt install postgrespro-std-14-docs postgrespro-std-14-docs-ru

sudo /opt/pgpro/std-14/bin/pg-wrapper links update

sudo /opt/pgpro/std-14/bin/pg-setup initdb -D /usr/local/pgsql/otklicc/data --locale=ru_RU.utf8 --lc-messages=en_US.utf8 -k

sudo /opt/pgpro/std-14/bin/pg-setup service enable

sudo /opt/pgpro/std-14/bin/pg-setup service start