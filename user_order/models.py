from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from userinterface.models import product as Product
from datetime import datetime

ORDER_CHOICES = (
    ("1",'ยังไม่ได้ชำระ'),
    ("2",'กำลังตรวจสอบสลิป'),
    ("3",'กำลังเตรียมสินค้า'),
    ("4",'กำลังนำสินค้าไปส่ง'),
    ("5",'ทำการส่งเรียบร้อย'),
    ("6",'ผู้ใช้รับสินค้าแล้ว'),
    ("7",'คำสั่งซื้อถูกยกเลิก'),
    ("8",'สลิปไม่ถูกต้อง'),
    )

class Order(models.Model):
    fullname = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=100,blank=True)
    address = models.CharField(max_length=255,blank=True)
    total = models.IntegerField()
    status = models.CharField(max_length=20,choices= ORDER_CHOICES,default=1)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True,blank=True,auto_now=True)
    complete = models.DateTimeField(null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.customer.username}'
    
    def save(self, *args, **kwargs):
        if self.status == "5":
            self.complete = datetime.now()
            super().save(*args, **kwargs)
        elif self.status == "3":
            order_detail = OrderDetail.objects.filter(order=self)
            for i in order_detail:
                i.product.stock -= i.amount
                i.save()
                i.product.save()
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

class OrderDetail(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    
    def sum(self):
        return self.price * self.amount

class Payment(models.Model):
    image = models.ImageField(upload_to='payment',blank=True)
    order = models.OneToOneField(Order,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.order}'
    
