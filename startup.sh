#!/bin/bash

if [ -z ${PORT+x} ]; 
then 
    export PORT=5000;
fi
if [ -z ${POSTGRES_HOST} ];
then
    export POSTGRES_HOST=127.0.0.1;
fi
if [ -z ${POSTGRES_PORT} ];
then
    export POSTGRES_PORT=5432;
fi
if [ -z ${POSTGRES_USER} ];
then
    export POSTGRES_USER=sdx;
fi
if [ -z ${POSTGRES_PASSWORD} ];
then
    export POSTGRES_PASSWORD=sdx;
fi
if [ -z ${POSTGRES_NAME} ];
then
    export POSTGRES_NAME=sdx;
fi
if [ "$SDX_DEV_MODE" = true ]
then
    python3 server.py
else
    gunicorn -b 0.0.0.0:$PORT server:app
fi