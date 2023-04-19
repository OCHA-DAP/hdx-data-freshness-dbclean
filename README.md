### Utility to clean Freshness Database
[![Build Status](https://github.com/OCHA-DAP/hdx-data-freshness-dbclean/actions/workflows/run-python-tests.yml/badge.svg)](https://github.com/OCHA-DAP/hdx-data-freshness-dbclean/actions/workflows/run-python-tests.yml) [![Coverage Status](https://coveralls.io/repos/github/OCHA-DAP/hdx-data-freshness-dbclean/badge.svg?branch=main&ts=1)](https://coveralls.io/github/OCHA-DAP/hdx-data-freshness-dbclean?branch=main)

This script cleans the freshness database.


### Usage

    python run.py [--db_url=] [--db_params=] [action]

action: 

- "clone" which creates a shallow clone of the database which only
has all the runs and one dataset and its resources per run for testing 
purposes.

- "clean" cleans the database by removing runs according to these rules:
  1. Keep a handful of runs around the end of each quarter all the way back to 
  the first run in 2017
  2. Keep daily runs going back 2 years
  3. Keep weekly runs from 2 to 4 years back
  4. Keep monthly runs for 4 years back and earlier