from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Worker(models.Model):
    firstname = models.CharField(max_length=255,blank=True)
    lastname = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=255,blank=True)
    specialization = models.CharField(max_length=255,blank=True)
    worker = models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self) -> str:
        return f'{self.worker}'

class WorkRequest(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255,blank=True)
    lastname = models.CharField(max_length=255,blank=True)
    car_part = models.CharField(max_length=255,blank=True)
    car_brand = models.CharField(max_length=255,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.customer}'
    

WORK_CHOICE = (
        ("1", 'รอรับอะไหล่'),
        ("2", 'กำลังซ่อม'),
        ("3", 'ซ่อมเสร็จสิ้น'),
        )

class AssignWork(models.Model):
    work_request = models.ForeignKey(WorkRequest, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices= WORK_CHOICE,default=1)
    def __str__(self) -> str:
        return f'{self.worker}'