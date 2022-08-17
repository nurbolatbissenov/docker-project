#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"


set -e

python manage.py makemigrations --noinput
python manage.py migrate --noinput

gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -w $GUNICORN_WORKERS -b 0.0.0.0:8000
