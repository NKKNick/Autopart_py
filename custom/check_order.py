from user_cart.models import Cart, CartDetail
from user_order.models import Order, Payment
from django.contrib.auth.models import User

from worker_app.models import Worker


def user_is_order(user):
    try:
        cart = Cart.objects.get(customer=user)
        have_Order = CartDetail.objects.filter(cart=cart)[0]     
        return True
    except :
        return False
    
def user_is_payment(id):
    try:
        order = Order.objects.get(pk=id)
        payment =Payment.objects.filter(order=order)[0]
        return True
    except:
        return False
    
def user_is_worker(user):
    try:
        worker = Worker.objects.get(worker=user)
        return True
    except:
        return False