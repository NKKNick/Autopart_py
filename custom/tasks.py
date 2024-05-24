# yourapp/tasks.py

from celery import shared_task
from django.utils import timezone
from user_order.models import Order


@shared_task
def delete_unpaid_orders():
    now = timezone.now()
    unpaid_orders = Order.objects.filter(payment_deadline__lt=now, status='1')
    count = unpaid_orders.count()
    unpaid_orders.delete()
    return f"Deleted {count} unpaid orders"
