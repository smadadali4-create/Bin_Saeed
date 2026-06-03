from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductSize


def cart_detail(request):
    cart = request.session.get('cart', {})
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
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
    })


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    size = request.POST.get('size', 'M')

    if size not in dict(Product.SIZE_CHOICES):
        size = 'M'

    product_size = ProductSize.objects.filter(product=product, size=size).first()
    max_stock = product_size.stock if product_size else 0

    cart = request.session.get('cart', {})

    key = f'{product_id}_{size}'

    if key in cart:
        if cart[key]['quantity'] < max_stock:
            cart[key]['quantity'] += 1
            messages.success(request, f'Increased {product.name} ({size}) quantity.')
        else:
            messages.warning(request, f'Not enough stock for {product.name} ({size}).')
    else:
        if max_stock > 0:
            cart[key] = {
                'product_id': product_id,
                'quantity': 1,
                'size': size,
            }
            messages.success(request, f'{product.name} ({size}) added to cart.')
        else:
            messages.warning(request, f'{product.name} ({size}) is out of stock.')

    request.session['cart'] = cart
    return redirect('cart:cart_detail')


def cart_remove(request, item_key):
    cart = request.session.get('cart', {})
    if item_key in cart:
        del cart[item_key]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
    return redirect('cart:cart_detail')


def cart_update(request, item_key):
    cart = request.session.get('cart', {})
    if item_key not in cart:
        return redirect('cart:cart_detail')

    quantity = request.POST.get('quantity', 1)
    size = request.POST.get('size', cart[item_key].get('size', 'M'))

    if size not in dict(Product.SIZE_CHOICES):
        size = cart[item_key].get('size', 'M')

    try:
        quantity = int(quantity)
        product = get_object_or_404(Product, id=cart[item_key]['product_id'])
        product_size = ProductSize.objects.filter(product=product, size=size).first()
        max_stock = product_size.stock if product_size else 0

        if quantity > 0 and quantity <= max_stock:
            cart[item_key]['quantity'] = quantity
            cart[item_key]['size'] = size
            request.session['cart'] = cart
            messages.success(request, 'Cart updated.')
        elif quantity <= 0:
            del cart[item_key]
            request.session['cart'] = cart
            messages.success(request, 'Item removed from cart.')
        else:
            messages.warning(request, f'Only {max_stock} in stock for size {size}.')
    except ValueError:
        messages.error(request, 'Invalid quantity.')

    return redirect('cart:cart_detail')
