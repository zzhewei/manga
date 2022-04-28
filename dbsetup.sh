#!/usr/bin/env bash
echo waiting for db in 50 secs...
sleep 50
python -m flask init
exec gunicorn -b :5000 --threads 4 app:app --preload