from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class product(models.Model):
  product_name = models.CharField(max_length=100)
  description = models.TextField()
  brand = models.CharField(max_length=100)
  price = models.IntegerField()
  cost = models.IntegerField(default=200)
  stock = models.IntegerField()
  picture = models.ImageField(upload_to="product",blank=True)

  def __str__(self) -> str:
    return f'{self.product_name}'
  
  def sumcost(self):
    return self.cost * self.stock
  

class AddStock(models.Model):
  product = models.ForeignKey(product,on_delete=models.DO_NOTHING)
  name = models.CharField(max_length=255,default='')
  stock = models.IntegerField()
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return f'{self.product} add stock {self.stock}'
  
