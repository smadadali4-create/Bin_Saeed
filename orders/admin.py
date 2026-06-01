from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'payment_method', 'payment_status_colored', 'status_colored', 'total', 'payment_proof_preview', 'order_actions', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    list_display_links = ['id', 'full_name']
    search_fields = ['full_name', 'phone', 'user__username', 'id']
    inlines = [OrderItemInline]
    readonly_fields = ['total', 'created_at', 'updated_at', 'user', 'full_name', 'phone', 'address', 'city', 'payment_method', 'payment_proof_preview']
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['confirm_orders', 'mark_shipped', 'mark_delivered', 'cancel_orders']
    fieldsets = (
        ('Customer Details', {
            'fields': ('user', 'full_name', 'phone', 'address', 'city')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'total', 'payment_proof_preview')
        }),
        ('Order Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def payment_status_colored(self, obj):
        if obj.payment_status == 'paid':
            return mark_safe('<span style="color: #28a745; font-weight: 600;">Paid</span>')
        return mark_safe('<span style="color: #ffc107; font-weight: 600;">Pending</span>')
    payment_status_colored.short_description = 'Payment'

    def status_colored(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'shipped': '#007bff',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html('<span style="color: {}; font-weight: 600;">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Status'

    def payment_proof_preview(self, obj):
        if obj.payment_proof:
            return mark_safe(f'<a href="{obj.payment_proof.url}" target="_blank"><img src="{obj.payment_proof.url}" style="width:50px;height:50px;object-fit:cover;border-radius:6px;border:1px solid rgba(212,175,55,0.3);" /></a>')
        return mark_safe('<span style="color:#666;">No proof</span>')
    payment_proof_preview.short_description = 'Proof'

    def order_actions(self, obj):
        btns = []
        if obj.status == 'pending':
            btns.append(f'<a href="{reverse("admin:confirm_order", args=[obj.id])}" class="button" style="background:#17a2b8;color:#fff;padding:4px 10px;border-radius:4px;text-decoration:none;font-size:11px;margin:2px;display:inline-block;">Confirm</a>')
            btns.append(f'<a href="{reverse("admin:cancel_order", args=[obj.id])}" class="button" style="background:#dc3545;color:#fff;padding:4px 10px;border-radius:4px;text-decoration:none;font-size:11px;margin:2px;display:inline-block;">Cancel</a>')
        elif obj.status == 'confirmed':
            btns.append(f'<a href="{reverse("admin:ship_order", args=[obj.id])}" class="button" style="background:#007bff;color:#fff;padding:4px 10px;border-radius:4px;text-decoration:none;font-size:11px;margin:2px;display:inline-block;">Ship</a>')
            btns.append(f'<a href="{reverse("admin:cancel_order", args=[obj.id])}" class="button" style="background:#dc3545;color:#fff;padding:4px 10px;border-radius:4px;text-decoration:none;font-size:11px;margin:2px;display:inline-block;">Cancel</a>')
        elif obj.status == 'shipped':
            btns.append(f'<a href="{reverse("admin:deliver_order", args=[obj.id])}" class="button" style="background:#28a745;color:#fff;padding:4px 10px;border-radius:4px;text-decoration:none;font-size:11px;margin:2px;display:inline-block;">Deliver</a>')
        return mark_safe(' '.join(btns)) if btns else mark_safe('<span style="color:#666;">—</span>')
    order_actions.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('confirm/<int:order_id>/', self.admin_site.admin_view(self.confirm_order_view), name='confirm_order'),
            path('ship/<int:order_id>/', self.admin_site.admin_view(self.ship_order_view), name='ship_order'),
            path('deliver/<int:order_id>/', self.admin_site.admin_view(self.deliver_order_view), name='deliver_order'),
            path('cancel/<int:order_id>/', self.admin_site.admin_view(self.cancel_order_view), name='cancel_order'),
        ]
        return custom_urls + urls

    def confirm_order_view(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.status = 'confirmed'
        order.save()
        messages.success(request, f'Order #{order.id} confirmed!')
        return redirect('admin:orders_order_changelist')

    def ship_order_view(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.status = 'shipped'
        order.save()
        messages.success(request, f'Order #{order.id} marked as shipped!')
        return redirect('admin:orders_order_changelist')

    def deliver_order_view(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.status = 'delivered'
        order.save()
        messages.success(request, f'Order #{order.id} delivered!')
        return redirect('admin:orders_order_changelist')

    def cancel_order_view(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} cancelled!')
        return redirect('admin:orders_order_changelist')

    def confirm_orders(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} order(s) confirmed.')
    confirm_orders.short_description = 'Confirm selected orders'

    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as shipped.')
    mark_shipped.short_description = 'Mark selected as shipped'

    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')
    mark_delivered.short_description = 'Mark selected as delivered'

    def cancel_orders(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} order(s) cancelled.')
    cancel_orders.short_description = 'Cancel selected orders'
