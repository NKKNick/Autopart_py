#!/usr/bin/env bash
# รันตอน Build เสร็จ
python manage.py migrate
python manage.py collectstatic --noinput