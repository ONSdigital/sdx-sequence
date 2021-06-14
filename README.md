# sdx-sequence

[![Build Status](https://github.com/ONSdigital/sdx-sequence/workflows/Build/badge.svg)](https://github.com/ONSdigital/sdx-sequence) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6e6856e9c191481ebeed8c10b70cfc16)](https://www.codacy.com/app/ons-sdc/sdx-sequence?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/sdx-sequence&amp;utm_campaign=Badge_Grade)

Scalable service for generating sequences for SDX.

## Prerequisites

A running instance of Postgres DB. The service connects to `postgres://sdx@sdxlocalhost:5432/sdx` by default.


## Installation
This application presently installs required packages from requirements files:
- `requirements.txt`: packages for the application, with hashes for all packages: see https://pypi.org/project/hashin/
- `test-requirements.txt`: packages for testing and linting

It's also best to use `pyenv` and `pyenv-virtualenv`, to build in a virtual environment with the currently recommended version of Python.  To install these, see:
- https://github.com/pyenv/pyenv
- https://github.com/pyenv/pyenv-virtualenv
- (Note that the homebrew version of `pyenv` is easiest to install, but can lag behind the latest release of Python.)

### Getting started
Once your virtual environment is set, install the requirements:
```shell
$ make build
```

To test, first run `make build` as above, then run:
```shell
$ make test
```

### Docker

```bash
$ docker build -t sdx-sequence
```

## Usage

Start the sdx-sequence service using the following command:

```shell
$ python server.py
```

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

The following envioronment variables can be set for non cloudfoundry use:

| Environment Variable           | Default                               | Description
|--------------------------------|---------------------------------------|----------------
| SDX_SEQUENCE_POSTGRES_HOST     | `127.0.0.1`                           | The PostgreSQL host
| SDX_SEQUENCE_POSTGRES_PORT     | `5432`                                | The PostgreSQL port
| SDX_SEQUENCE_POSTGRES_NAME     | `sdx`                                 | The PostgreSQL database
| SDX_SEQUENCE_POSTGRES_USER     | `sdx`                                 | The PostgreSQL user
| SDX_SEQUENCE_POSTGRES_PASSWORD | `sdx`                                 | The PostgreSQL password

For cloudfoundry only the DB_URL needs to be set in vcap services the format:

postgres://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME

### License

Copyright ©‎ 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.
