from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import models
from customers.models import Customer
from orders.models import Order
from products.models import Product


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summary_report(request):
    user = request.user
    total_customers = Customer.objects.filter(owner = user).count()
    total_products = Product.objects.filter(owner = user).count()
    total_orders = Order.objects.filter(owner = user).count()
    shipped_orders = Order.objects.filter(owner = user,status = 'shipped').count()
    total_sales = Order.objects.filter(owner = user,status = 'shipped').aggregate(
        total = models.Sum('total_price')
    )['total'] or 0

    return Response({
        'total_customers':total_customers,
        'total_products':total_products,
        'total_orders':total_orders,
        'shipped_orders':shipped_orders,
        'total_sales':total_sales,
    })

from datetime import timedelta, datetime
from django.utils.timezone import now
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chart_data(request):
    user = request.user
    range_type = request.GET.get('range', 'daily')

    # 选择时间截断函数和起始时间
    if range_type == 'monthly':
        trunc_fn = TruncMonth
        start_date = now() - timedelta(days=180)
    elif range_type == 'weekly':
        trunc_fn = TruncWeek
        start_date = now() - timedelta(weeks=12)
    else:
        trunc_fn = TruncDay
        start_date = now() - timedelta(days=30)

    # 销售额趋势
    sales_qs = (
        Order.objects.filter(owner=user, status='shipped', created_at__gte=start_date)
        .annotate(period=trunc_fn('created_at'))
        .values('period')
        .annotate(total=Sum('total_price'))
        .order_by('period')
    )

    sales_trend = [
        {'date': item['period'].strftime('%Y-%m-%d'), 'total': float(item['total'])} for item in sales_qs
    ]

    # 订单状态分布
    status_qs = (
        Order.objects.filter(owner=user)
        .values('status')
        .annotate(count=Count('id'))
    )

    order_status = [
        {'status': item['status'], 'count': item['count']} for item in status_qs
    ]

    return Response({
        'sales_trend': sales_trend,
        'order_status': order_status,
    })
