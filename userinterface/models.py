from django.db import models


# Create your models here.
class product(models.Model):
  product_name = models.CharField(max_length=100)
  description = models.TextField()
  brand = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10,decimal_places=2)
  stock = models.IntegerField()
  picture = models.ImageField(upload_to="product",blank=True)

  def __str__(self) -> str:
    return f'{self.product_name}'
