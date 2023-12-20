from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_cart.models import *
from userinterface.models import product as Product


@login_required
def cart(request):
    count = 0
    total = 0
    try:
        # Try to get the existing cart for the user
        cart = Cart.objects.get(customer=request.user)
    except Cart.DoesNotExist:
        # If the cart doesn't exist, create a new one
        cart = Cart.objects.create(customer=request.user, cart_id=create_cart(request))

    try:
        cart_detail = CartDetail.objects.filter(cart=cart)
        for detail in cart_detail:
            count += detail.amount  
            total += detail.product.price * detail.amount
    except CartDetail.DoesNotExist:
        # Handle the case where there are no cart details
        cart = None
        cart_detail = None

    return render(request, "cart.html", {'count': count, 'total': total, 'cartDetail': cart_detail})


def create_cart(req):
    cart = req.session.session_key
    if not cart:
        cart.req.session.create()
    return cart

@login_required(login_url="/login")
def add_cart(req,id):
    product = Product.objects.get(pk=id)
    try:  #กรณีมี order อยู่แล้ว
        cart = Cart.objects.get(cart_id=create_cart(req),customer=req.user)
    except Cart.DoesNotExist: #กรณีไม่มี order
        cart = Cart.objects.create(
            cart_id= create_cart(req),
            customer= req.user
        )
        cart.save()
    try: #ถ้าสั่งซำ้ จะเพิ่มสินค้าตัวนั้น
        cartdetail = CartDetail.objects.get(product=product,cart=cart)
        if cartdetail.amount < cartdetail.product.stock:
            cartdetail.amount += 1
            cartdetail.save()
            return redirect('/')
    except CartDetail.DoesNotExist: #ถ้าไม่เคยสั่งจะ set ค่า amount เป็น 1
        cartdetail = CartDetail.objects.create(
            product=product,
            cart = cart,
            amount = 1,
        )
        cartdetail.save()

    return redirect('/')

@login_required
def delete_cart(req,id):
    product = Product.objects.get(pk=id)
    cart = Cart.objects.get(cart_id=create_cart(req),customer=req.user)
    cartDetail=CartDetail.objects.get(product=product,cart=cart)
    cartDetail.delete()
    return redirect("/cart")