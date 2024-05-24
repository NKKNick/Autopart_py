from django.urls import path

from usersapp import views


urlpatterns = [
    path("login",views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('profile',views.user_profile,name='user_profile'),
]
