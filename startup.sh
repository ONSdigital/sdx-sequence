#!/bin/bash

if [ -z ${PORT+x} ]; 
then 
    export PORT=5000;
    export POSTGRES_HOST=127.0.0.1;
    export POSTGRES_PORT=5432;
    export POSTGRES_USER=sdx;
    export POSTGRES_PASSWORD=sdx;
    export POSTGRES_NAME=sdx;

fi

if [ "$SDX_DEV_MODE" = true ]
then
    python3 server.py
else
    gunicorn -b 0.0.0.0:$PORT server:app
fi