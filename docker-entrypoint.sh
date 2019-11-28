#!/bin/sh
set -ex

until psql postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db/$POSTGRES_DB -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

python manage.py collectstatic --no-input

python manage.py migrate --no-input

exec gunicorn cupweb.wsgi:application --bind 0.0.0.0:8000 --workers 3
