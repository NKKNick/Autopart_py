from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Worker(models.Model):
    image = models.ImageField(upload_to="worker",blank=True)
    firstname = models.CharField(max_length=255,blank=True)
    lastname = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=255,blank=True)
    specialization = models.CharField(max_length=255,blank=True)
    worker = models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self) -> str:
        return f'{self.worker}'
    
    def get_assignments_end_dates(self):
        assignments = AssignWork.objects.filter(worker=self)
        end_dates = [assignment.end_date for assignment in assignments]
        return end_dates

    def get_latest_assignment_end_date(self):
        latest_assignment = AssignWork.objects.filter(worker=self).filter(status='2').order_by('-end_date').first()
        if latest_assignment:
            return latest_assignment.end_date
        return None

REQUEST_CHOICE = (
    ("1","รอยืนยัน"),
    ("2","กำลังดำเนินการ"),
    ("3","เสร็จสิ้น"),
    ("4","ถูกยกเลิก"),
)
class WorkRequest(models.Model):
    admin = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255,blank=True)
    lastname = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=255,blank=True,null=True)
    car_part = models.CharField(max_length=255,blank=True)
    car_brand = models.CharField(max_length=255,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=20,choices= REQUEST_CHOICE,default=1)
    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'
    

WORK_CHOICE = (
        ("1", 'กำลังดำเนินการ'),
        ("2", 'กำลังดำเนินการ'),
        ("3", 'เสร็จสิ้น'),
        ("4", 'ถูกยกเลิก'),
        ("5", 'เลยกำหนด'),
)

class AssignWork(models.Model):
    work_request = models.ForeignKey(WorkRequest, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True,null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=20,choices= WORK_CHOICE,default=2)
    def __str__(self) -> str:
        return f'{self.worker} ทำงานของ {self.work_request}'

class Bill(models.Model):
    work = models.OneToOneField(WorkRequest,on_delete=models.CASCADE)
    cost = models.IntegerField()