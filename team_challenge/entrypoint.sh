#!/bin/sh

python manage.py collectstatic --no-input

gunicorn team_challenge.wsgi:application --bind 0.0.0.0:8000