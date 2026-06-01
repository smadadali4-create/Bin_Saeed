from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category


def product_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')

    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'products': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })
