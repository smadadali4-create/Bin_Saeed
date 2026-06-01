from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from products.models import Product


@staff_member_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    pending_payments = Order.objects.filter(payment_status='pending').count()
    recent_orders = Order.objects.order_by('-created_at')[:10]
    low_stock_products = Product.objects.filter(stock__lt=5, available=True)[:5]

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'pending_payments': pending_payments,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'title': 'Dashboard - BIN SAEED OUTLET',
    }
    return render(request, 'admin/dashboard.html', context)
