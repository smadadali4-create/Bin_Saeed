from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from products.models import Product


def home(request):
    featured_products = Product.objects.filter(available=True)[:8]
    return render(request, 'core/index.html', {
        'featured_products': featured_products,
        'contact_phone': settings.CONTACT_PHONE,
        'contact_whatsapp': settings.CONTACT_WHATSAPP,
    })


def about(request):
    return render(request, 'core/about.html', {
        'contact_phone': settings.CONTACT_PHONE,
        'contact_whatsapp': settings.CONTACT_WHATSAPP,
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        messages.success(request, f'Thank you {name}! Your message has been received. We will get back to you shortly.')
    return render(request, 'core/contact.html', {
        'contact_phone': settings.CONTACT_PHONE,
        'contact_whatsapp': settings.CONTACT_WHATSAPP,
        'contact_email': settings.CONTACT_EMAIL,
    })
