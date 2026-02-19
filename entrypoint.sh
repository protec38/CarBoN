#!/usr/bin/env bash

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate --no-input
poetry run python superuser_creation.py
poetry run gunicorn -b :8003 settings.wsgi
# poetry run python manage.py runserver 0.0.0.0:8001
