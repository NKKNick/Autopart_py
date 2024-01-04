from django.db import models
from django.contrib.auth.models import User
from userinterface.models import *

class Order(models.Model):
    fullname = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=255,blank=True)
    total = models.IntegerField()
    customer = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    created = models.DateTimeField(auto_now_add=True)

class OrderDetail(models.Model):
    product = models.CharField(max_length=255)
    price = models.IntegerField()
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,)
    

