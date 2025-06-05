from django.shortcuts import render
from rest_framework import viewsets, permissions

from customers.models import Customer
from customers.serializers import CustomerSerializer


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(owner = self.request.user)

    #每个用户只能访问自己的客户信息
    def get_queryset(self):
        return  Customer.objects.filter(owner = self.request.user)