### Utility to clean Freshness Database
[![Build Status](https://github.com/OCHA-DAP/hdx-data-freshness-dbclean/actions/workflows/run-python-tests.yml/badge.svg)](https://github.com/OCHA-DAP/hdx-data-freshness-dbclean/actions/workflows/run-python-tests.yml) [![Coverage Status](https://coveralls.io/repos/github/OCHA-DAP/hdx-data-freshness-dbclean/badge.svg?branch=main&ts=1)](https://coveralls.io/github/OCHA-DAP/hdx-data-freshness-dbclean?branch=main)

This script cleans the freshness database.


### Usage

    python run.py [-db/--db_url=] [-dp/--db_params=] [action]

Either db_url or db_params must be provided or the environment variable DB_URL
must be set. db_url or DB_URL are of form: 
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