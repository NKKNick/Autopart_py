from django.db import models
from django.contrib.auth.models import User
from userinterface.models import product

# Create your models here.
class Cart(models.Model):
  cart_id = models.CharField(max_length=100,blank=True)
  customer = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
  def __str__(self) -> str:
    return f"{self.customer.username}"

class CartDetail(models.Model):
  product = models.ForeignKey(product,on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
  amount = models.IntegerField()

  def __str__(self) -> str:
    return f"{self.product.product_name} : {self.amount}"