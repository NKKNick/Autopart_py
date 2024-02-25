from django.http import HttpResponse
from django.shortcuts import redirect, render
from custom.line_notify import send_text
from user_cart.models import Cart, CartDetail
from userinterface.models import *
from .models import product as Product


# Create your views here.
def home(req):
    obj = product.objects.all()
    sorted_items = sorted(obj, key=lambda x: (x.stock == 0, x.stock))
    return render(req,"home.html",{"product":sorted_items})

def detail(req,id):
    obj = product.objects.get(pk=id)
    return render(req,"product_details.html",{"product":obj})

def contact(req):
    return render(req,'contact.html')

def stock(req):
    product = Product.objects.all()
    for i in product:
        if i.stock <= 0:
            message = f"{i.product_name} เหลือ {i.stock}"
            send_text(message)
    return render(req, 'testnot.html')

def search_product(req):
    search = req.GET['search']
    if search:
        product = Product.objects.filter(product_name__contains=search)
        return render(req,'search_product.html',{'product':product})
    else:
        return redirect('/')
