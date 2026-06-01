from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Category, Product


@staff_member_required
def add_product(request):
    categories = Category.objects.all()
    new_category_name = request.POST.get('new_category')

    if request.method == 'POST':
        if new_category_name:
            cat_slug = slugify(new_category_name)
            category, created = Category.objects.get_or_create(
                name=new_category_name,
                defaults={'slug': cat_slug}
            )
            if created:
                messages.success(request, f'Category "{new_category_name}" created!')
            return redirect('admin_add_product')

        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        available = request.POST.get('available') == 'on'

        if not name:
            messages.error(request, 'Product name is required.')
        elif not category_id:
            messages.error(request, 'Please select a category.')
        elif not price:
            messages.error(request, 'Price is required.')
        else:
            base_slug = slugify(name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            product = Product.objects.create(
                name=name,
                slug=slug,
                category_id=category_id,
                price=price,
                stock=int(stock) if stock else 0,
                description=description or '',
                image=image,
                available=available,
            )
            messages.success(request, f'Product "{name}" posted successfully!')
            return redirect('admin_add_product')

    return render(request, 'products/admin_add_product.html', {
        'categories': categories,
        'title': 'Add Product - BIN SAEED OUTLET',
    })
