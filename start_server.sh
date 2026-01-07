#!/bin/sh

export PYTHONPYCACHEPREFIX=./pycache/

python3 -X pycache_prefix=./pycache/ server.py
