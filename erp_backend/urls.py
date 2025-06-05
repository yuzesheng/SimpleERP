"""
URL configuration for erp_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/users/',include('users.urls')),#加入用户模块路由
        path('api/customers/',include('customers.urls')),#加入客户模块路由
        path('api/products/',include('products.urls')),#加入产品模块
        path('api/orders/',include('orders.urls')),#加入订单模块
        path('api/reports/',include('reports.urls')) #加入报表模块
]
