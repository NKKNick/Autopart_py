from django.urls import path

from worker_app import views


urlpatterns = [
    path("repair",views.assign_work,name="assign_work"),
    path("work/display",views.display_work,name="display_work"),
] 