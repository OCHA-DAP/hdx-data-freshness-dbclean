### Utility to clean Freshness Database
[![Build Status](https://github.com/OCHA-DAP/hdx-data-freshness-dbclean/actions/workflows/run-python-tests.yml/badge.svg)](https://github.com/OCHA-DAP/hdx-data-freshness-dbclean/actions/workflows/run-python-tests.yml)
[![Coverage Status](https://codecov.io/gh/OCHA-DAP/hdx-data-freshness-dbclean/branch/main/graph/badge.svg?token=JpWZc5js4y)](https://codecov.io/gh/OCHA-DAP/hdx-data-freshness-dbclean)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


This script cleans the freshness database.


### Usage

    python -m hdx.freshness.dbactions [-db/--db_uri=] [-dp/--db_params=] [action]

Either db_uri or db_params must be provided or the environment variable DB_URI
must be set. db_uri or DB_URI are of form: 
postgresql+psycopg://user:password@host:port/database

db_params is of form:
database=XXX,host=X.X.X.X,username=XXX,password=XXX,port=1234,
ssh_host=X.X.X.X,ssh_port=1234,ssh_username=XXX,
ssh_private_key=/home/XXX/.ssh/keyfile

action: 

- "clone" which creates a shallow clone of the database which only
has all the runs and one dataset and its resources per run for testing 
purposes.

- "clean" (the default) cleans the database by removing runs according to these 
rules:
  1. Keep a handful of runs around the end of each quarter all the way back to 
  the first run in 2017
  2. Keep daily runs going back 2 years
  3. Keep weekly runs from 2 to 4 years back
  4. Keep monthly runs for 4 years back and earlier