from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name