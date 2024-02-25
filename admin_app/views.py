from django.shortcuts import redirect, render
from django.contrib.auth.decorators import permission_required
from admin_app.forms import ProductForm
from custom.check_order import user_is_payment
from user_order.models import Order, OrderDetail, Payment
from userinterface.models import product as Product
from django.contrib.auth.models import User
# Create your views here.
@permission_required("admin",login_url="/")
def dashboard(req):
    order=Order.objects.order_by('-created')
    return render(req,'admin_order.html',{"order":order})

@permission_required("admin",login_url="/")
def update_order(req,id):
    order = Order.objects.get(pk=id)
    if req.method == "POST":
        status = req.POST["status"]
        order.status = status
        order.save()
        return redirect('/dashboard')

@permission_required('admin' ,login_url="/")
def admin_ord(req,id):
    order = Order.objects.get(pk=id)
    orderdetail = OrderDetail.objects.filter(order=order)
    total = 0
    for i in orderdetail:
        total += i.amount * i.price
    if user_is_payment(id=order.id):
        payment = Payment.objects.get(order=order)
        return render(req,'admin_detail.html',{'orders':orderdetail,'total':total,'payment':payment,'order':order})
    
    return render(req,'admin_detail.html',{'orders':orderdetail,'total':total,'order':order})

@permission_required('admin' ,login_url="/")
def accept_order(req,id):
    order=Order.objects.get(pk=id)
    order.status = "3"
    order.save()
    orderdetail = OrderDetail.objects.filter(order=order)
    for i in orderdetail:
        product = Product.objects.get(pk=i.product.id)
        product.stock = int(i.product.stock - i.amount)
        product.save()
    return redirect('/dashboard')

@permission_required('admin' ,login_url="/")
def cancel_order(req,id):
    order=Order.objects.get(pk=id)
    order.status = "7"
    order.save()
    return redirect('/dashboard')

@permission_required('admin' ,login_url="/")
def manage_user(req):
    user = User.objects.all()
    return render(req,'manageuser.html',{'users':user})

@permission_required('admin' ,login_url="/")
def admin_product(req):
    product = Product.objects.all()
    return render(req,'admin_product.html',{'product':product})

@permission_required('admin' ,login_url="/")
def product_delete(req,id):
    product = Product.objects.get(pk=id)
    product.delete()
    return redirect(admin_product)

def create_product(req):
    if req.method == "POST":
        forms = ProductForm(req.POST,req.FILES)
        if forms.is_valid():
            forms.save()
            return redirect(admin_product)
    else:
        forms = ProductForm()
    return render(req,'create_product.html',{'form':forms})

def update_product(req,id):
    product = Product.objects.get(pk=id)
    if req.method == "POST":
        form = ProductForm(req.POST,req.FILES,instance=product)
        form.save()
        return redirect(admin_product)
    else:
        form = ProductForm(instance=product)
    return render(req,"update_product.html",{"form":form,"product":product})
