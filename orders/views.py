from django.shortcuts import render
from rest_framework import viewsets, permissions

from orders.models import Order
from orders.serializers import OrderSerializer


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return  Order.objects.filter(owner = self.request.user)