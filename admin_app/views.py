from django.db.models import Sum, Max
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import permission_required
from admin_app.forms import ProductForm, WorkerForm
from custom.check_order import user_is_order, user_is_payment
from user_cart.models import Cart, CartDetail
from user_order.models import Order, OrderDetail, Payment
from userinterface.models import product as Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from worker_app.models import AssignWork, Bill, WorkRequest, Worker
# Create your views here.
from django.template.defaulttags import register
from django.core.paginator import Paginator
from django.utils import timezone
import calendar
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



@permission_required("admin",login_url="/")
def dashboard(req):
    order=Order.objects.order_by('-created')
    return render(req,'admin_order.html',{"order":order})



#order function
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


#manage user function
@permission_required('admin' ,login_url="/")
def manage_user(req):
    user = User.objects.all()
    page = req.GET.get("page")
    paginator=Paginator(user,5)
    user=paginator.get_page(page)
    return render(req,'admin_user.html',{'users':user})

@permission_required('admin' ,login_url="/")
def create_user(req):
    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']
        email = req.POST['email']
        if username=='' or email=='' or password=='':
            messages.warning(req,'กรุณาป้อนข้อมูลให้ครบ')
            return redirect("/dashboard/create/user")
        else:
            if User.objects.filter(username=username).exists():
                messages.warning(req,"ชื่อผู้ใช้นี้มีอยู่แล้ว")
                return redirect("/dashboard/create/user")
            elif User.objects.filter(email=email).exists():
                messages.warning(req,"อีเมลนี้ถูกใช้แล้ว")
                return redirect("/dashboard/create/user")
            else:
                user=User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
                return redirect("/dashboard/manage/user")
    return render(req,'create_user.html')

@permission_required('admin' ,login_url="/")
def create_worker(req,id):
    user = User.objects.get(pk=id)
    if req.method == "POST":
        form = WorkerForm(req.POST,req.FILES)
        if form.is_valid():
            form.save()
            user.is_staff = True
            user.save()
            return redirect("/dashboard/manage/user")
    else:
        form = WorkerForm()
    return render(req,'create_worker.html',{'form':form,'users':user})


#product function
@permission_required('admin' ,login_url="/")
def admin_product(req):
    product = Product.objects.all()
    return render(req,'admin_product.html',{'product':product})

@permission_required('admin' ,login_url="/")
def product_delete(req,id):
    product = Product.objects.get(pk=id)
    product.delete()
    return redirect(admin_product)

@permission_required('admin' ,login_url="/")
def create_product(req):
    if req.method == "POST":
        forms = ProductForm(req.POST,req.FILES)
        if forms.is_valid():
            forms.save()
            return redirect(admin_product)
    else:
        forms = ProductForm()
    return render(req,'create_product.html',{'form':forms})

@permission_required('admin' ,login_url="/")
def update_product(req,id):
    product = Product.objects.get(pk=id)
    if req.method == "POST":
        form = ProductForm(req.POST,req.FILES,instance=product)
        form.save()
        return redirect(admin_product)
    else:
        form = ProductForm(instance=product)
    return render(req,"update_product.html",{"form":form,"product":product})

#worker function

@permission_required('admin' ,login_url="/")
def work_display(req):
    work = WorkRequest.objects.all().filter(status="1")
    return render(req,'admin_work.html',{'worker':work})

def search_user(req):
    search = req.GET['query']
    user = User.objects.filter(username__icontains=search)
    if user.exists():
        return render(req,'admin_user.html',{'users':user})
    else:
        user = User.objects.filter(email__icontains=search)
        if user.exists():
            return render(req,'admin_user.html',{'users':user})
        else:
            return render(req,'admin_user.html',{'users':user})

@permission_required('admin' ,login_url="/")
def worker_show(req,id):
    work_id = id
    worker=Worker.objects.all()
    work_counts = {}
    for work in worker:
        work_count = AssignWork.objects.filter(worker=work).filter(status="2").count()
        work_counts[work] = work_count
    
    return render(req,"worker_show.html",{'worker':worker,"work_id":work_id,"work_count":work_counts})

@permission_required('admin' ,login_url="/")
def worker_show2(req):
    worker=Worker.objects.all()
    work_counts = {}
    for work in worker:
        work_count = AssignWork.objects.filter(worker=work).filter(status="2").count()
        work_counts[work] = work_count
    
    return render(req,"worker_show2.html",{'worker':worker,"work_count":work_counts})

@permission_required('admin' ,login_url="/")
def worker_assign(req,work_id,worker_id):
    worker = Worker.objects.get(pk=worker_id)
    work = WorkRequest.objects.get(pk=work_id)
    assign = AssignWork.objects.create(
        work_request = work,
        worker = worker,
        end_date = work.end_date,
    )
    work.status = "2"
    work.save()
    assign.save()
    return redirect("/dashboard/display/assign")

@permission_required('admin' ,login_url="/")
def assign_display(req):
    assign = AssignWork.objects.filter(status=2).order_by('-start_date')
    return render(req,'assign_display.html',{'assign':assign})

@permission_required('admin' ,login_url="/")
def delete_assign(req,id):
    assign = AssignWork.objects.get(pk=id)
    assign.delete()
    return redirect('/dashboard/display/assign')

@permission_required('admin' ,login_url="/")
def report(req):
    return render(req,'report.html')

@permission_required('admin' ,login_url="/")
def pos(req):
    product = Product.objects.all()
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

    return render(req, "pos.html", {'products':product,'count': count, 'total': total, 'cart': cart_detail})

@permission_required('admin' ,login_url="/")
def admin_cart(req, id):
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
            return redirect('/dashboard/pos')
        else:
            return redirect('/dashboard/pos')
    
    except CartDetail.DoesNotExist:
        cart_detail = CartDetail.objects.create(
            product=product,
            cart=cart,
            amount=1,
        )
        return redirect('/dashboard/pos')

@permission_required('admin' ,login_url="/")
def delete_pos(req,id):
    product = Product.objects.get(pk=id)
    cart = Cart.objects.get(customer=req.user)
    cartDetail=CartDetail.objects.get(product=product,cart=cart)
    cartDetail.delete()
    return redirect("/dashboard/pos")

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
                #ลดสต็อก
                '''
                product = Product.objects.get(pk=i.product.id)
                product.stock = int(i.product.stock - order_detail.amount)
                product.save()
                '''
                i.delete()
            cart.delete()
            return redirect('/order/payment/%d'%order.id)
        return render(req,'order.html')
    return redirect('/')

def inc_cart(req,id):
    cart = CartDetail.objects.get(pk=id)
    if cart.amount < cart.product.stock:
        cart.amount += 1
        cart.save()
        return redirect('/dashboard/pos')
    else :
        return redirect('/dashboard/pos')

def dec_cart(req,id):
    cart = CartDetail.objects.get(pk=id)
    if cart.amount > 1:
        cart.amount -= 1
        cart.save()
        return redirect('/dashboard/pos')
    else :
        cart.delete()
        return redirect('/dashboard/pos')

@permission_required('admin' ,login_url="/")   
def create_bill(req,id):
    work = WorkRequest.objects.get(pk=id)
    if req.method == "POST":
        cost = req.POST['cost']
        bill = Bill.objects.create(
                work=work,
                cost=cost
            )
        bill.save()
        return redirect("/dashboard/display/assign")
    return redirect("/")

@permission_required('admin' ,login_url="/")  
def admin_work_detail(req,id):
    assign = AssignWork.objects.get(pk=id)
    work = WorkRequest.objects.get(pk=assign.work_request.id)
    return render(req,'workdetail.html',{'work':work,'assign':assign})

@permission_required('admin' ,login_url="/")  
def repair(req):
    if req.method == "POST":
        firstname = req.POST["firstname"]
        lastname = req.POST["lastname"]
        car_part = req.POST["carpart"]
        car_brand = req.POST["car_brand"]
        phone = req.POST["phone"]
        note = req.POST["note"]
        end_date = req.POST["enddate"]
        workreq=WorkRequest.objects.create(
            customer=req.user,
            firstname=firstname,
            lastname=lastname,
            car_part=car_part,
            car_brand=car_brand,
            phone = phone,
            note = note,
            end_date = end_date,
        )
        workreq.save()
        return redirect('/dashboard/display/worker')
    return render(req,'create_repair.html')

@permission_required('admin' ,login_url="/") 
def delete_repair(req,id):
    work_req = WorkRequest.objects.get(pk=id)
    work_req.delete()
    return redirect('/dashboard/display/worker')

@permission_required('admin' ,login_url="/")  
def admin_calendar(req,worker_id):
    cur = timezone.now().date()
    year = cur.year
    month = cur.month
    cal = calendar.monthcalendar(year,month)
    day = []
    worker = Worker.objects.get(pk=worker_id)
    assign = AssignWork.objects.filter(worker=worker).filter(status='2').order_by('end_date')
    count = AssignWork.objects.filter(worker=worker).filter(status='2').count()
    day.append(0)
    for row in cal:
        for cell in row:
            day.append(cell)
    context = {
        'year':year,
        'month':month,
        'cal':cal,
        'day':day,
        'cur':cur.day,
        'cur_mon':cur.month,
        'cur_year':cur.year,
        'assign':assign,
        'count':count,
    }
    return render(req, 'work_cal2.html', context)

@permission_required('admin' ,login_url="/")  
def admin_calendar2(req,year,month):
    cur = timezone.now().date()
    cal = calendar.monthcalendar(year,month)
    day = []
    worker = Worker.objects.get(worker=req.user)
    assign = AssignWork.objects.filter(worker=worker).filter(status='2').order_by('end_date')
    day.append(0)
    for row in cal:
        for cell in row:
            day.append(cell)
    context = {
        'year':year,
        'month':month,
        'cal':cal,
        'day':day,
        'cur':cur.day,
        'cur_mon':cur.month,
        'cur_year':cur.year,
        'assign':assign,
    }
    return render(req, 'work_cal2.html', context)

@permission_required('admin' ,login_url="/")  
def next_month(req):
    current_date = timezone.now().date()
    next_month = current_date + timezone.timedelta(days=30)
    return redirect(f'/dashboard/cal/{next_month.month}/{next_month.year}')

@permission_required('admin' ,login_url="/")  
def prev_month(req):
    current_date = timezone.now().date()
    prev_month = current_date - timezone.timedelta(days=30) 
    return redirect(f'/dashboard/cal/{prev_month.month}/{prev_month.year}')

@permission_required('admin' ,login_url="/")  
def now_month(req):
    current_date = timezone.now().date()
    return redirect(f'/dashboard/cal/{current_date.month}/{current_date.year}')

from django.db.models.functions import TruncMonth

@permission_required('admin' ,login_url="/")  
def report(req):
    #ยอดขายตามสินค้า
    order = OrderDetail.objects.filter(order__status='5').values('product__product_name').annotate(
        total_amount=Sum('amount'),
    )
    #ยอดขายทั้งหมด groupby month
    monthly_sales = OrderDetail.objects.filter(order__status='5').annotate(month=TruncMonth('updated')).values('month').annotate(
        total_sales=Sum('price')
    ).order_by('month')
    monthly_cost = OrderDetail.objects.annotate(month=TruncMonth('updated')).values('month').annotate(
        total_sales=Sum('product__cost')
    ).order_by('month')
    # Get the current date
    current_date = timezone.now()
    current_year = current_date.year
    current_month = current_date.month

    # ยอดขายเดือนนี้
    this_month_sales = OrderDetail.objects.filter(
        created__year=current_year,
        created__month=current_month,
        order__status='5',
    ).aggregate(total_sales=Sum('price'))
    this_month_cost = OrderDetail.objects.filter(
        created__year=current_year,
        created__month=current_month,
    ).aggregate(total_sales=Sum('product__cost'))
    order_details = OrderDetail.objects.filter(
        created__year=current_year,
        created__month=current_month
    )

    worker = Worker.objects.all().count()
    product = Product.objects.all().count()
    order_count = Order.objects.all().filter(status='2').count()
    p_name = []
    total_amount = []
    for i in order:
        p_name.append(i.get('product__product_name'))
        total_amount.append(i.get('total_amount'))

    context={
        'order':order,
        'product':product,
        'p_name':p_name,
        'total_amount':total_amount,
        'monthly_sales': monthly_sales,
        'monthly_cost': monthly_cost,
        'worker':worker,
        'product':product,
        'order_count':order_count,
        'this_month_sales':this_month_sales,
        'this_month_cost':this_month_cost,
    }
    return render(req,'report.html',context)

@permission_required('admin' ,login_url="/")  
def admin_change_status(req,id):
    if req.method == "POST":
        assign = AssignWork.objects.get(pk=id)
        assign.status = req.POST["status"]
        work_req = assign.work_request
        work_req.status = req.POST["status"]
        work_req.save()
        assign.save()
        print(assign.status,assign.work_request.status)
        return redirect('/dashboard/display/assign')
    return redirect('/dashboard/display/assign')
