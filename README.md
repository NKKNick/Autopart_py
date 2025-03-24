django run
python manage.py runserver

celery command (cronjob local)
### 1st terminal
celery -A autopart worker --loglevel=info
### 2st terminal
celery -A autopart beat --loglevel=info
