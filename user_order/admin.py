from django.contrib import admin

from user_cart.models import Cart
from user_order.models import *

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Payment)