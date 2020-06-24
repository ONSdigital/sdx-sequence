### Unreleased
  - Add openapi.yml
  
### 2.6.4 2020-06-09
  - Remove Cloudfoundry deployment files
  
### 2.6.3 2020-05-21  
  - Updated packages

### 2.6.2 2019-11-08
  - Add python 3.8 to travis builds

### 2.6.1 2019-09-26
  - Update packages, including Werkzeug that had a security vulnerability

### 2.6.0 2019-05-31
  - Remove python 3.4 and 3.5 from travis builds
  - Add python 3.7 to travis builds
  - Upgrade urllib3, Jinja2 and sqlalchemy to fix security issues.
  - Upgrade various packages.

### 2.5.1 2019-02-19
  - Update packages to fix security issues
  - Fix logging to output in a standard way

### 2.5.0 2018-01-04
  - Add /info healthcheck endpoint

### 2.4.0 2017-11-21
  - Add Cloudfoundry deployment files
  - Remove use of sdx-common for logging

### 2.3.0 2017-11-01
  - Begin using pytest as default test runner
  - Add all service config to config file

### 2.2.0 2017-09-25
  - Removed SDX common clone in docker
  - Remove JSON logging
  - Allow batches of sequence numbers to be requested

### 2.1.0 2017-07-25
  - Change all instances of ADD to COPY in Dockerfile
  - Remove use of SDX_HOME variable in makefile
  - Fix database tests on travis

### 2.0.0 2017-07-10
  - Use Postgres backend via SQLAlchemy ORM.
  - Add environment variable details to README
  - Correct license attribution
  - Add codacy badge
  - Adding sdx-common functionality
  - Updating logger format using sdx-common
  - Fix Dockerfile to load dependencies before using them.
  - Add support for codecov to see unit test coverage
  - Update and pin version of sdx-common to 0.7.0

### 1.3.1 2017-03-15
  - Log version number on startup
  - Add change log

### 1.3.0 2016-12-13
  - Add new `/json-sequence` endpoint to support census processing

### 1.2.0 2016-10-24
  - Add new `/healthcheck` endpoint

### 1.1.0 2016-09-19
  - Add configurable log level

### 1.0.0 2016-07-13
  - Initial release
