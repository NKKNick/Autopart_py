#!/usr/bin/env bash
# รันตอน Build เสร็จ
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput