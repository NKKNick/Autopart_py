from django.urls import path

from worker import views



urlpatterns = [
    path("try",views.justtry),
]
