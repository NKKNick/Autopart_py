from django.urls import path
from userinterface import views

urlpatterns = [
    path("",views.home,name="home"),
    path('product/detail/<int:id>',views.detail ,name="detail"),
    path('contact',views.contact ,name="contact"),
    path('search',views.search_product ,name="search_product"),
    path('req/detail/<int:id>',views.req_detail ,name="req_detail"),
    path('req/display',views.req_display ,name="req_display"),
]
