import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from custom.check_order import user_is_order

from django.contrib.auth.models import User
from custom.line_notify import send_image
from user_order.models import Order,OrderDetail,Payment
from user_cart.models import Cart,CartDetail
from userinterface.models import product as Product
from usersapp.models import UserProfile
# Create your views here.

    
@login_required(login_url="/login")
def order(req):
    if user_is_order(user=req.user):
        if req.method == "POST":
            fullname = req.POST['fullname']
            phone = req.POST['phone']
            address = req.POST['address']
            cart = Cart.objects.get(customer=req.user)
            cartOb = CartDetail.objects.filter(cart=cart)
            total = 0
            for i in cartOb:
                total += i.product.price * i.amount
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
                    product=i.product,
                    amount = i.amount,
                    price = i.product.price,
                    order = order,
                )
                order_detail.save()
                i.delete()
            cart.delete()
            return redirect(f'/order/payment/{order.id}')
        try:
            profile = UserProfile.objects.get(user=req.user)
            return render(req,'orderwp.html',{'profile':profile})
        except:
            return render(req,'order.html')
    return redirect('/')

def payment(req,id):
    order=Order.objects.get(pk=id)
    if req.method == "POST":
        image = req.FILES.get('payment')
        payment = Payment.objects.create(
            image=image,
            order=order,
        )
        payment.save()
        #เปลี่ยน status จาก "ยังไม่ได้ชำระ" เป็น "ตรวจสอบสลิป"
        order.status = "2"
        order.save()
        # message = f'\nผู้ซื้อ: {order.fullname}\nที่อยู่: {order.address}\nเบอร์ติดต่อ: {order.phone}\nจำนวนเงินที่ต้องชำระ: {order.total}'
        # payment_url = payment.image.url.replace('/','',1)
        # image_path = payment_url     
        # send_image(message,image_path)
        return redirect('/order/complete')
    return render(req,'payment.html',{'order':order})

@login_required(login_url="/login")
def order_detail(req,id):
    order = Order.objects.get(pk=id)
    if order.customer == req.user:
        obj=OrderDetail.objects.filter(order=order)
        earliest =order.created+datetime.timedelta(days=2)
        latest = order.created+datetime.timedelta(days=5)
        context = {
            'orders':obj,
            'order':order,
            'early':earliest,
            'late':latest,
        }
        return render(req,'orderdetails.html',context)
    else:
        redirect("order/history")

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

@login_required(login_url="/login")
def order_history(req):
    orders=Order.objects.filter(customer=req.user).order_by('-created')
    return render(req,"order_history.html",{"orders":orders})
