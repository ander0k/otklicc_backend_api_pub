#!/bin/bash

ps augx | grep "uvicorn main:app" |grep "api_otkli_cc_privkey.pem" | awk '{print $2}' | xargs kill
