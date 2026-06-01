from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Order, OrderItem
from products.models import Product
from .utils import send_order_confirmation_to_admin


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    cart_items = []
    total = 0
    for key, item_data in cart.items():
        product = get_object_or_404(Product, id=item_data['product_id'], available=True)
        item_total = product.price * item_data['quantity']
        total += item_total
        cart_items.append({
            'key': key,
            'product': product,
            'quantity': item_data['quantity'],
            'size': item_data.get('size', 'M'),
            'total': item_total,
        })

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        payment_method = request.POST.get('payment_method')

        if not all([full_name, phone, address, city, payment_method]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'payment_methods': settings.PAYMENT_METHODS,
            })

        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            payment_method=payment_method,
            total=total,
        )

        for key, item_data in cart.items():
            product = get_object_or_404(Product, id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price,
                size=item_data.get('size', 'M'),
            )

            if product.stock >= item_data['quantity']:
                product.stock -= item_data['quantity']
                product.save()

        request.session['cart'] = {}

        send_order_confirmation_to_admin(order)

        if payment_method == 'cash':
            messages.success(request, 'Order placed successfully! Your order will be delivered soon.')
            return redirect('orders:order_confirmation', order_id=order.id)
        else:
            messages.info(request, 'Please upload your payment screenshot to confirm your order.')
            return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'payment_methods': settings.PAYMENT_METHODS,
    })


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment_info = settings.PAYMENT_METHODS.get(order.payment_method, {})
    payment_whatsapp_text = f'Order #{order.id} - Rs.{order.total} paid via {order.get_payment_method_display()}'
    return render(request, 'orders/order_confirmation.html', {
        'order': order,
        'payment_info': payment_info,
        'payment_whatsapp_text': payment_whatsapp_text,
    })


def order_history(request):
    phone = request.GET.get('phone', '')
    orders = []
    if phone:
        orders = Order.objects.filter(phone=phone)
        if not orders:
            messages.info(request, 'No orders found for this phone number.')
    return render(request, 'orders/order_history.html', {'orders': orders, 'search_phone': phone})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


def upload_payment_proof(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST' and request.FILES.get('payment_proof'):
        order.payment_proof = request.FILES['payment_proof']
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.save()
        messages.success(request, '✅ Payment proof received! Order #' + str(order.id) + ' is now CONFIRMED. We will process it shortly.')
        return redirect('orders:order_detail', order_id=order.id)
    return redirect('orders:order_detail', order_id=order.id)
