#!/bin/sh
while ! mysqladmin ping -h"$DB_HOST" --silent;
do
    sleep 1;
done

python manage.py migrate
python manage.py ensure_admin
python manage.py fill_employees_data
python manage.py collectstatic --noinput
gunicorn -w 2 -b 0.0.0.0:8000 tl_group_test.wsgi --timeout 3600 --workers 4