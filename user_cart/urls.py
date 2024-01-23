from django.urls import path
from user_cart import views


urlpatterns = [
    path('cart',views.cart,name='cart'),
    path('cart/add/<int:id>',views.add_cart,name='addcart'),
    path('cart/delete/<int:id>',views.delete_cart,name='delete_cart'),
    path('cart/deliver',views.deliver,name='deliver'),
    ]