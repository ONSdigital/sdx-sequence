# sdx-sequence

[![Build Status](https://travis-ci.org/ONSdigital/sdx-sequence.svg?branch=master)](https://travis-ci.org/ONSdigital/sdx-sequence)

Scalable service for generating sequences for SDX (backed by MongoDB).

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

# Example

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
