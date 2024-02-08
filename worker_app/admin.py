from django.contrib import admin
from worker_app.models import *
# Register your models here.
admin.site.register(Worker)
admin.site.register(Work)
admin.site.register(WorkDetail)