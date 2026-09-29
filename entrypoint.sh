#!/usr/bin/env bash

poetry run python manage.py migrate --no-input
poetry run python manage.py collectstatic --noinput
poetry run superuser_creation.py
poetry run gunicorn -b 0.0.0.0:8000 settings.wsgi $GUNICORN_EXTRA_ARGS