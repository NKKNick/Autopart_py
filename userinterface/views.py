from django.http import HttpResponse
from django.shortcuts import redirect, render
from custom.check_order import profile_is_exist
from custom.line_notify import send_text
from user_cart.models import Cart, CartDetail
from userinterface.models import *
from usersapp.models import UserProfile
from worker_app.models import AssignWork, Bill, WorkRequest
from .models import product as Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def home(req):
    obj = product.objects.all()
    sorted_items = sorted(obj, key=lambda x: (x.stock == 0, x.stock))
    page = req.GET.get("page")
    paginator = Paginator(sorted_items,6)
    sorted_items = paginator.get_page(page)
    return render(req,"home.html",{"product":sorted_items})

def detail(req,id):
    obj = product.objects.get(pk=id)
    return render(req,"product_details.html",{"product":obj})

def contact(req):
    return render(req,'contact.html')

def search_product(req):
    search = req.GET['search']
    if search:
        product = Product.objects.filter(product_name__contains=search)
        return render(req,'search_product.html',{'product':product})
    else:
        return redirect('/')

@login_required(login_url="/login")
def req_display(req):
    if profile_is_exist(user=req.user.id):
        profile = UserProfile.objects.get(user=req.user.id)
        w_req = WorkRequest.objects.filter(phone=profile.phone)
        w_sort = w_req.order_by('-created')
        page = req.GET.get("page")
        paginator=Paginator(w_sort,5)
        work=paginator.get_page(page)
        context ={
            'w_req':work,
        }
        return render(req,'req_display.html',context)
    else:
        return redirect('/profile')

@login_required(login_url="/login")
def req_detail(req,id):
    w_req = WorkRequest.objects.get(pk=id)
    try:
        assign = AssignWork.objects.get(work_request=w_req.id)
        try:
            bill = Bill.objects.get(work=w_req)
            return render(req,'req_detail.html',{"w_req":w_req,"assign":assign,"bill":bill})
        except:
            return render(req,'req_detail.html',{"w_req":w_req,"assign":assign})
    except:
        return render(req,'req_detail.html',{"w_req":w_req})