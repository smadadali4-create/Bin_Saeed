from django.conf import settings
from products.models import Product


def cart_total(request):
    cart = request.session.get('cart', {})
    total_items = sum(item['quantity'] for item in cart.values())
    total_price = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id, available=True)
            total_price += product.price * item['quantity']
        except Product.DoesNotExist:
            pass
    return {
        'cart_total_items': total_items,
        'cart_total_price': total_price,
    }
