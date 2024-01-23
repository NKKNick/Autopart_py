from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_order.models import *
from user_cart.models import Cart,CartDetail
from userinterface.models import product as Product
# Create your views here.
@login_required(login_url="/login")
def order(req):
    if req.method == "POST":
        fullname = req.POST['fullname']
        phone = req.POST['phone']
        address = req.POST['address']
        cart = Cart.objects.get(customer=req.user)
        cartOb = CartDetail.objects.filter(cart=cart)
        total = 0
        for i in cartOb:
            total += i.product.price * i.amount
        if total <= 0:
            return HttpResponse('ไม่สามารถเข้าถึงหน้านี้ได้')
        else:
            order = Order.objects.create(
                fullname=fullname,
                phone = phone,
                address = address,
                total = total,
                customer = req.user
            )
            order.save()
            #save order_detail และ ลดสต็อก
            for i in cartOb:
                order_detail = OrderDetail.objects.create(
                    product=i.product.product_name,
                    amount = i.amount,
                    price = i.product.price,
                    order = order,
                )
                order_detail.save()
                #ลดสต็อก
                product = Product.objects.get(pk=i.product.id)
                product.stock = int(i.product.stock - order_detail.amount)
                product.save()
                i.delete()
            cart.delete
        return render(req,'order_complete.html')

    return render(req,'order.html')

@login_required(login_url="/login")
def pickup(req):
    count = 0
    total = 0
    try:
        cart = Cart.objects.get(customer=req.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(customer=req.user)

    try:
        cart_detail = CartDetail.objects.filter(cart=cart)
        for detail in cart_detail:
            count += detail.amount  
            total += detail.product.price * detail.amount
            
    except CartDetail.DoesNotExist:
        cart = None
        cart_detail = None

    return render(req, "pickup.html", {'count': count, 'total': total, 'cartDetail': cart_detail})

@login_required(login_url="/login")
def order_complete(req):
    return render(req,'order_complete.html')