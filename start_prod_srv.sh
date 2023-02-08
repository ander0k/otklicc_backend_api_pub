#!/bin/bash

cd /opt/otklicc/app/

mv /opt/otklicc/app/uvicorn.log /opt/otklicc/log/uvicorn_$(date +"%Y%m%d_%H%M%S%N").log

touch /opt/otklicc/app/uvicorn.log

/home/api_otklicc/.local/bin/uvicorn main:app --host api.otkli.cc --port 8080 --ssl-keyfile=$OTKLICC_API_PRIVKEY --ssl-certfile=$OTKLICC_API_CERT_FULLCHAIN >>/opt/otklicc/app/uvicorn.log 2>&1  &