from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
        ('raast', 'Raast Transfer'),
        ('cash', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, default='M')

    def __str__(self):
        size_display = dict(self.SIZE_CHOICES).get(self.size, self.size)
        return f"{self.quantity} x {self.product.name} ({size_display})"

    def get_cost(self):
        return self.price * self.quantity
