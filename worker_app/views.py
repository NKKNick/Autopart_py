from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test,login_required
from django.urls import reverse
from custom.check_order import user_is_worker
from worker_app.models import AssignWork, Worker
import calendar
from django.utils import timezone
# Create your views here.
@login_required(login_url='/login')
def display_work(req):
    if user_is_worker(user=req.user):
        worker = Worker.objects.get(worker=req.user)
        assign = AssignWork.objects.filter(worker=worker).filter(status='1')
        return render(req,'display_work2.html',{'work':assign,'worker':worker})
    return redirect('/')

@login_required(login_url='/login')
def work_detail(req,id):
    if user_is_worker(user=req.user):
        assign = AssignWork.objects.get(pk=id)
        return render(req,'work_detail.html',{'assign':assign})
    return redirect('/')

@login_required(login_url='/login')
def change_status(req,id):
    if user_is_worker(user=req.user):
        if req.method == "POST":
            assign = AssignWork.objects.get(pk=id)
            assign.status = req.POST["status"]
            work_req = assign.work_request
            work_req.status = req.POST["status"]
            assign.note = req.POST["note"]
            work_req.save()
            assign.save()
            return redirect('/calendar')
        return redirect(work_detail)
    


@login_required(login_url='/login')
def work_calendar(req):
    if user_is_worker(user=req.user):
        cur = timezone.now().date()
        year = cur.year
        month = cur.month
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
        return render(req, 'work_calendar.html', context)

@login_required(login_url='/login')
def work_calendar2(req,year,month):
    if user_is_worker(user=req.user):
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
        return render(req, 'work_calendar.html', context)
from django.core.paginator import Paginator
@login_required(login_url='/login')
def work_hist(req):
    if user_is_worker(user=req.user):
        worker = Worker.objects.get(worker=req.user)
        assign=AssignWork.objects.filter(worker=worker).filter(status='3').order_by('-end_date')
        page = req.GET.get("page")
        paginator = Paginator(assign,3)
        assign = paginator.get_page(page)
        context = {
            'assign':assign,
        }
        return render(req,'work_history.html', context)
    
@login_required(login_url='/login')
def next_month(req):
    current_date = timezone.now().date()
    next_month = current_date + timezone.timedelta(days=30)
    return redirect(f'/calendar/{next_month.month}/{next_month.year}')

@login_required(login_url='/login')
def prev_month(req):
    current_date = timezone.now().date()
    prev_month = current_date - timezone.timedelta(days=30) 
    return redirect(f'/calendar/{prev_month.month}/{prev_month.year}')

@login_required(login_url='/login')
def now_month(req):
    current_date = timezone.now().date()
    return redirect(f'/calendar/{current_date.month}/{current_date.year}')