from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test,login_required
from custom.check_order import user_is_worker
from worker_app.models import WorkRequest

# Create your views here.
@login_required(login_url='/login')
def assign_work(req):
    if req.method == "POST":
        firstname = req.POST["firstname"]
        lastname = req.POST["lastname"]
        car_part = req.POST["carpart"]
        car_brand = req.POST["car_brand"]
        workreq=WorkRequest.objects.create(
            customer=req.user,
            firstname=firstname,
            lastname=lastname,
            car_part=car_part,
            car_brand=car_brand,
        )
        workreq.save()
        return redirect('/')
    return render(req,'assign.html')


def display_work(req):
    if user_is_worker(user=req.user):
        work=WorkRequest.objects.all()
        return render(req,'display_work2.html',{'work':work})
    return redirect('/')