from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_cart.models import *
from userinterface.models import product as Product


@login_required(login_url="/login")
def cart(request):
    count = 0
    total = 0
    try:
        cart = Cart.objects.get(customer=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(customer=request.user)

    try:
        cart_detail = CartDetail.objects.filter(cart=cart)
        for detail in cart_detail:
            count += detail.amount  
            total += detail.product.price * detail.amount
            
    except CartDetail.DoesNotExist:
        cart = None
        cart_detail = None
    return render(request, "cart.html", {'count': count, 'total': total, 'cartDetail': cart_detail})


def create_cart(req):
    cart = req.session.session_key
    if not cart:
        cart.req.session.create()
    return cart

@login_required(login_url="/login")
def add_cart(req, id):
    product = Product.objects.get(pk=id)
    try:
        # ดึงข้อมูลที่มีอยู่แล้ว
        cart = Cart.objects.get(customer=req.user)
    except Cart.DoesNotExist:
        # ถ้าไม่มีสร้างใหม่
        cart = Cart.objects.create(customer=req.user)

    try:
        cart_detail = CartDetail.objects.get(product=product, cart=cart)
        if cart_detail.amount < cart_detail.product.stock:
            cart_detail.amount += 1
            cart_detail.save()
            return redirect('/')

    except CartDetail.DoesNotExist:
        cart_detail = CartDetail.objects.create(
            product=product,
            cart=cart,
            amount=1,
        )
        return redirect('/')

@login_required(login_url="/login")
def delete_cart(req,id):
    product = Product.objects.get(pk=id)
    cart = Cart.objects.get(customer=req.user)
    cartDetail=CartDetail.objects.get(product=product,cart=cart)
    cartDetail.delete()
    return redirect("/cart")