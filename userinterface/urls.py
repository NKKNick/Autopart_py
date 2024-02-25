from django.urls import path
from userinterface import views

urlpatterns = [
    path("",views.home,name="home"),
    path('stock',views.stock ,name="stock"),
    path('product/detail/<int:id>',views.detail ,name="detail"),
    path('contact',views.contact ,name="contact"),
    path('search',views.search_product ,name="search_product"),
]
