from django.contrib import admin

from user_cart.models import Cart
from user_order.models import Order

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)