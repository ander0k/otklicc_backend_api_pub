#!/bin/bash

uvicorn main:app --host 0.0.0.0 --port 8080 --reload --log-level=debug --ssl-keyfile=$OTKLICC_API_PRIVKEY --ssl-certfile=$OTKLICC_API_CERT_FULLCHAIN