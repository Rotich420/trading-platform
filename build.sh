#!/usr/bin/env bash

pip install -r requirements.txt

cd trading_platform

python manage.py collectstatic --noinput
python manage.py migrate