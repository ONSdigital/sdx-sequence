#!/bin/bash

if [ -z ${PORT+x} ]; 
then 
    export PORT=5000;
fi
if [ -z ${SDX_SEQUENCE_POSTGRES_HOST} ];
then
    export SDX_SEQUENCE_POSTGRES_HOST=127.0.0.1;
fi
if [ -z ${SDX_SEQUENCE_POSTGRES_PORT} ];
then
    export SDX_SEQUENCE_POSTGRES_PORT=5432;
fi
if [ -z ${SDX_SEQUENCE_POSTGRES_USER} ];
then
    export SDX_SEQUENCE_POSTGRES_USER=sdx;
fi
if [ -z ${SDX_SEQUENCE_POSTGRES_PASSWORD} ];
then
    export SDX_SEQUENCE_POSTGRES_PASSWORD=sdx;
fi
if [ -z ${SDX_SEQUENCE_POSTGRES_NAME} ];
then
    export SDX_SEQUENCE_POSTGRES_NAME=sdx;
fi
if [ "$SDX_DEV_MODE" = true ]
then
    python3 server.py
else
    gunicorn -b 0.0.0.0:$PORT server:app
fi