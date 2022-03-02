#!/usr/bin/env bash

python manage.py db migrate -m "first"
python manage.py db upgrade
python app.py