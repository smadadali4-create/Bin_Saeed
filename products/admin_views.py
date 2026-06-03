from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Category, Product, ProductImage, ProductSize


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
        description = request.POST.get('description')
        image = request.FILES.get('image')
        images = request.FILES.getlist('images')
        available = request.POST.get('available') == 'on'
        stock_s = int(request.POST.get('stock_s', 0))
        stock_m = int(request.POST.get('stock_m', 0))
        stock_l = int(request.POST.get('stock_l', 0))
        total_stock = stock_s + stock_m + stock_l

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
                stock=total_stock,
                description=description or '',
                image=image,
                available=available,
            )

            ProductSize.objects.create(product=product, size='S', stock=stock_s)
            ProductSize.objects.create(product=product, size='M', stock=stock_m)
            ProductSize.objects.create(product=product, size='L', stock=stock_l)

            for img in images:
                ProductImage.objects.create(product=product, image=img)

            messages.success(request, f'Product "{name}" posted successfully!')
            return redirect('admin_add_product')

    return render(request, 'products/admin_add_product.html', {
        'categories': categories,
        'title': 'Add Product - BIN SAEED OUTLET',
    })
