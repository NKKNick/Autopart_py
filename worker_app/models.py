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
    
class Work(models.Model):
    worker_id = models.ForeignKey(Worker,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.worker_id}'

class WorkDetail(models.Model):
    work_id = models.ForeignKey(Work,on_delete=models.CASCADE)
    car_part = models.CharField(max_length=255,blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True,blank=True)
    wating = 0
    reparing = 1
    done = 2
    STATUS_CHOICES = (
        (wating, 'Wating'),
        (reparing, 'Reparing'),
        (done, 'Done'),
        )
    status = models.SmallIntegerField(choices=STATUS_CHOICES,blank=True,default=wating)