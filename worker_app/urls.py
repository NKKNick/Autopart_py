from django.urls import path

from worker_app import views


urlpatterns = [
    path("work",views.assign_work),
] 