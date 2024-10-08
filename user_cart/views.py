from django.http import HttpResponse
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

@login_required(login_url="/login")
def add_cart(req, id):
    product = Product.objects.get(pk=id)
    try:
        cart = Cart.objects.get(customer=req.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(customer=req.user)

    try:
        cart_detail = CartDetail.objects.get(product=product, cart=cart)
        if cart_detail.amount < cart_detail.product.stock:
            cart_detail.amount += 1
            cart_detail.save()
            return redirect('/')
        else:
            return redirect('/cart')

    except CartDetail.DoesNotExist:
        cart_detail = CartDetail.objects.create(
            product=product,
            cart=cart,
            amount=1,
        )
        return redirect('/')

@login_required(login_url="/login")
def delete_cart(req,id):
    CartDetail.objects.get(pk=id).delete()
    return redirect("/cart")

@login_required(login_url="/login")
def deliver(req):
    if req.method == 'POST':
        deliver = req.POST.get('deli_se')
        if deliver == "sendhome":
            return redirect('/order')
        elif deliver == "pickup":
            return redirect('/pickup')
        else:
            return redirect('/cart')

@login_required(login_url="/login")   
def inc_cart(req,id):
    cart = CartDetail.objects.get(pk=id)
    if cart.amount < cart.product.stock:
        cart.amount += 1
        cart.save()
        return redirect('/cart')
    else :
        return redirect('/cart')

@login_required(login_url="/login")
def dec_cart(req,id):
    cart = CartDetail.objects.get(pk=id)
    if cart.amount > 1:
        cart.amount -= 1
        cart.save()
        return redirect('/cart')
    else :
        cart.delete()
        return redirect('/cart')