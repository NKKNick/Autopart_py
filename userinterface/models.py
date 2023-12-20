from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class product(models.Model):
  product_name = models.CharField(max_length=100)
  description = models.TextField()
  brand = models.CharField(max_length=100)
  price = models.IntegerField()
  stock = models.IntegerField()
  picture = models.ImageField(upload_to="product",blank=True)

  def __str__(self) -> str:
    return f'{self.product_name}'
  

