from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Order, OrderItem
from cart.models import Cart


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if cart.get_total_items() == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        payment_method = request.POST.get('payment_method')

        if not all([full_name, phone, address, city, payment_method]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'payment_methods': settings.PAYMENT_METHODS,
            })

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            payment_method=payment_method,
            total=cart.get_total_price(),
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

            product = cart_item.product
            if product.stock >= cart_item.quantity:
                product.stock -= cart_item.quantity
                product.save()

        cart.items.all().delete()

        if payment_method == 'cash':
            messages.success(request, 'Order placed successfully! Your order will be delivered soon.')
            return redirect('orders:order_confirmation', order_id=order.id)
        else:
            messages.info(request, 'Please upload your payment screenshot to confirm your order.')
            return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'payment_methods': settings.PAYMENT_METHODS,
    })


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment_info = settings.PAYMENT_METHODS.get(order.payment_method, {})
    payment_whatsapp_text = f'Order #{order.id} - Rs.{order.total} paid via {order.get_payment_method_display()}'
    return render(request, 'orders/order_confirmation.html', {
        'order': order,
        'payment_info': payment_info,
        'payment_whatsapp_text': payment_whatsapp_text,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def upload_payment_proof(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST' and request.FILES.get('payment_proof'):
        order.payment_proof = request.FILES['payment_proof']
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.save()
        messages.success(request, '✅ Payment proof received! Order #' + str(order.id) + ' is now CONFIRMED. We will process it shortly.')
        return redirect('orders:order_detail', order_id=order.id)
    return redirect('orders:order_detail', order_id=order.id)
