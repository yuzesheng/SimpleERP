from django.contrib.auth.models import User
from django.db import models

from customers.models import Customer
from products.models import Product


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ('new','新建'),
        ('shipped','已发货'),
        ('cancelled','已取消'),
    )
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='new')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def  __str__(self):
        return f'订单 #{self.id} - {self.customer.name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_item_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name}*{self.quantity}'
