#!/bin/ash


echo "running"

python manage.py migrate 

exec "$@"