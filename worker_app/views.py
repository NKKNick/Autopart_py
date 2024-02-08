from django.shortcuts import render

# Create your views here.
def assign_work(req):
    return render(req,'assign.html')