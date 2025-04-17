#!/usr/bin/env bash
# รันตอน Build เสร็จ
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell << END
import os
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username=os.environ['DJANGO_SU_NAME']).exists():
    User.objects.create_superuser(
        os.environ['DJANGO_SU_NAME'],
        os.environ['DJANGO_SU_EMAIL'],
        os.environ['DJANGO_SU_PASSWORD']
    )
END