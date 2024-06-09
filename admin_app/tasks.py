# yourapp/tasks.py

from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from user_order.models import Order


@shared_task
def delete_unpaid_orders():
    now = timezone.now()
    unpaid_orders = Order.objects.filter(status='1')
    if unpaid_orders.exists():
        for i in unpaid_orders:
            expire_order = i.created + timedelta(days=1)
            if expire_order <= now:
                count = i.id
                i.delete()
                return f"ลบออเดอร์ที่ไม่ชำระเงิน order_id: {count} "
    count = unpaid_orders.count()
    return f"ตอนนี้มีออเดอร์ที่ยังไม่ชำระเงิน: {count} "
