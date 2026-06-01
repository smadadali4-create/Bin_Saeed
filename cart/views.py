from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Increased {product.name} quantity in cart.')
        else:
            messages.warning(request, f'Not enough stock for {product.name}.')
    else:
        cart_item.quantity = 1
        cart_item.save()
        messages.success(request, f'{product.name} added to cart.')

    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart:cart_detail')


@login_required
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = request.POST.get('quantity', 1)

    try:
        quantity = int(quantity)
        if quantity > 0 and quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
        elif quantity <= 0:
            cart_item.delete()
            messages.success(request, f'{cart_item.product.name} removed from cart.')
        else:
            messages.warning(request, f'Only {cart_item.product.stock} in stock.')
    except ValueError:
        messages.error(request, 'Invalid quantity.')

    return redirect('cart:cart_detail')
