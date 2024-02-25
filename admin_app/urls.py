from django.urls import path
from admin_app import views

urlpatterns = [
    path("dashboard",views.dashboard,name='dashboard'),
    path("dashboard/status/<int:id>",views.update_order,name='dash_status'),
    path("dashboard/order/<int:id>",views.admin_ord,name="dash_detail"),
    path("dashboard/accept/<int:id>",views.accept_order,name="accept_order"),
    path("dashboard/cancel/<int:id>",views.cancel_order,name="cancel_order"),
    path("dashboard/manage/user",views.manage_user,name="manage_user"),
    path("dashboard/product",views.admin_product,name="admin_product"),
    path("dashboard/product/delete/<int:id>",views.product_delete,name="product_delete"),
    path("dashboard/product/create",views.create_product,name="product_create"),
    path("dashboard/product/update/<int:id>",views.update_product,name="product_update"),
]