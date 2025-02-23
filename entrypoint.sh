#!/usr/bin/env bash

poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate --no-input
poetry run python superuser_creation.py
poetry run gunicorn -b :8000 settings.wsgi