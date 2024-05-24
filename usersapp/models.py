from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    image = models.ImageField(upload_to="userprofile",blank=True)
    firstname = models.CharField(max_length=255,blank=True)
    lastname = models.CharField(max_length=255,blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=255,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'