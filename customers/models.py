from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customer(models.Model):
    owner = models.ForeignKey(User,on_delete= models.CASCADE,related_name='customers')
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100,blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20,blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name