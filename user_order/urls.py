from django.urls import path

from user_order import views


urlpatterns = [
    path("order",views.order,name='order'),
    path("pickup",views.pickup,name='pickup'),
    path("order/complete",views.order_complete,name='orderC'),
    path("order/history",views.order_history,name='orderH'),
    path("order/<int:id>",views.order_detail,name='orderDetail'),
] 