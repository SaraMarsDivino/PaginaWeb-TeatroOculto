#!/usr/bin/env sh
set -eu

# Ensure Django settings are resolvable for management commands
: "${DJANGO_SETTINGS_MODULE:=teatro_project.settings}"
export DJANGO_SETTINGS_MODULE

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
