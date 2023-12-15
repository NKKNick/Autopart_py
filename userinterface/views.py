from django.http import HttpResponse
from django.shortcuts import render
from custom.line_notify import send_line_notification

from userinterface.models import product


# Create your views here.
def home(req):
    obj = product.objects.all()
    return render(req,"home.html",{"product":obj})

def detail(req,id):
    obj = product.objects.get(pk=id)
    return render(req,"product_details.html",{"product":obj})


def stock(req):
    obj = product.objects.all()
    for i in obj:
        if i.stock <= 0:
            message = f"{i.product_name} เหลือ {i.stock}"
            send_line_notification(message)
    return render(req, 'testnot.html')