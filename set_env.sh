#!/bin/bash
export SQLALCHEMY_DATABASE_URI="postgresql://api.otkli.cc@db.otkli.cc:6432/db_otklicc?application_name=api.otkli.cc app"

export DOMAIN=localhost
# DOMAIN=local.dockertoolbox.tiangolo.com
# DOMAIN=localhost.tiangolo.com
# DOMAIN=dev.otkli.cc
export STACK_NAME="otkli-cc"
export TRAEFIK_PUBLIC_NETWORK="traefik-public"
export TRAEFIK_TAG="otkli.cc"
export TRAEFIK_PUBLIC_TAG="traefikpublic"
export DOCKER_IMAGE_BACKEND="otklicc_backend"
export DOCKER_IMAGE_CELERYWORKER="otklicc_celeryworker"
export DOCKER_IMAGE_FRONTEND="otklicc_frontend"
# Backend
export PROJECT_NAME="otklicc"
export SECRET_KEY=""
export FIRST_SUPERUSER=""
export FIRST_SUPERUSER_PASSWORD=""
export SMTP_TLS="True"
export SMTP_PORT="465"
export SMTP_HOST=""
export SMTP_USER=""
export SMTP_PASSWORD=""
export EMAILS_FROM_EMAIL=""
export USERS_OPEN_REGISTRATION="False"
export SENTRY_DSN=""
# Flower
export FLOWER_BASIC_AUTH=""

# Postgres
export POSTGRES_SERVER="db.otkli.cc"
export POSTGRES_USER="api.otkli.cc"
#POSTGRES_PASSWORD=
export POSTGRES_DB="db_otklicc"

# PgAdmin
export PGADMIN_LISTEN_PORT="5050"
export PGADMIN_DEFAULT_EMAIL=""
export PGADMIN_DEFAULT_PASSWORD=""
