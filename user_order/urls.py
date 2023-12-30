from django.urls import path

from user_order import views


urlpatterns = [
    path("hello",views.hello)
] 