#!/bin/sh
set -e
aerich upgrade
python -m app.seed
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
