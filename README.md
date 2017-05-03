# sdx-sequence

[![Build Status](https://travis-ci.org/ONSdigital/sdx-sequence.svg?branch=master)](https://travis-ci.org/ONSdigital/sdx-sequence)

Scalable service for generating sequences for SDX (backed by MongoDB).

## Prerequisites

A running instance of Postgres DB. The service connects to `postgres://sdx@sdxlocalhost:5432/sdx` by default.


## Installation

Using virtualenv and pip, create a new environment and install within using:

    $ pip install -r requirements.txt

It's also possible to install within a container using docker. From the sdx-sequence directory:

    $ docker build -t sdx-sequence .

## Usage

Start the sdx-sequence service using the following command:

    python server.py

## API

There are three endpoints for the three types of sequences:
 * `GET /sequence`
 * `GET /batch-sequence`
 * `GET /image-sequence`

There is also a health check endpoint, which returns a json response with key/value pairs describing the service state:
 * `GET /healthcheck`

## Example

Curl a request to any one of the endpoints:
```
curl http://localhost:5000/sequence
```

The response should look something like:
```
{
    sequence_no: 1000
}
```

## Configuration

The following envioronment variables can be set:

| Environment Variable    | Default                               | Description
|-------------------------|---------------------------------------|----------------
| POSTGRES_HOST           | `127.0.0.1`                           | The PostgreSQL host
| POSTGRES_PORT           | `5432`                                | The PostgreSQL port
| POSTGRES_NAME           | `sdx`                                 | The PostgreSQL database
| POSTGRES_USER           | `sdx`                                 | The PostgreSQL user
| POSTGRES_PASSWORD       | `sdx`                                 | The PostgreSQL password

