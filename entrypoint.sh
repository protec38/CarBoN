#!/usr/bin/env bash

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate --no-input
poetry run gunicorn -b :8000 -t 0 settings.wsgi