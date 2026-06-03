from django.core.mail import send_mail
from django.conf import settings


def _get_customer_email(order):
    if order.user and order.user.email:
        return order.user.email
    if order.email:
        return order.email
    return None


def send_order_confirmation_to_admin(order):
    subject = f'New Order #{order.id} - {order.full_name}'
    message = f"""
New order placed on {settings.SITE_NAME}

Order ID: #{order.id}
Customer: {order.full_name}
Phone: {order.phone}
Email: {order.email or 'N/A'}
Address: {order.address}, {order.city}
Payment: {order.get_payment_method_display()}
Total: Rs. {order.total}

Admin dashboard: https://smadadali4.pythonanywhere.com/admin/orders/order/
"""
    send_mail(
        subject,
        message,
        settings.CONTACT_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=True,
    )


def send_order_confirmation_to_customer(order):
    to_email = _get_customer_email(order)
    if not to_email:
        return

    subject = f'Order Confirmed - #{order.id} - {settings.SITE_NAME}'
    message = f"""
Dear {order.full_name},

Thank you for your order! Your order has been placed successfully.

Order Details:
Order ID: #{order.id}
Total: Rs. {order.total}
Payment Method: {order.get_payment_method_display()}
Status: {order.get_status_display()}

We will process your order shortly. You will receive updates as your order status changes.

Track your order: https://smadadali4.pythonanywhere.com/orders/history/

Thank you for shopping at {settings.SITE_NAME}!
Contact us: {settings.CONTACT_PHONE}
"""
    send_mail(
        subject,
        message,
        settings.CONTACT_EMAIL,
        [to_email],
        fail_silently=True,
    )


def send_status_update_to_customer(order):
    to_email = _get_customer_email(order)
    if not to_email:
        return

    status_messages = {
        'confirmed': 'Your order has been confirmed and will be processed shortly.',
        'shipped': 'Your order has been shipped and is on its way!',
        'delivered': 'Your order has been delivered. Thank you for shopping with us!',
        'cancelled': 'Your order has been cancelled. Please contact us for details.',
    }

    message = status_messages.get(order.status, f'Your order status has been updated to: {order.get_status_display()}')

    subject = f'Order #{order.id} - {order.get_status_display()}'
    full_message = f"""
Dear {order.full_name},

{message}

Order Details:
Order ID: #{order.id}
Total: Rs. {order.total}
Payment: {order.get_payment_method_display()}
Status: {order.get_status_display()}

Track your order: https://smadadali4.pythonanywhere.com/orders/history/

Thank you for shopping at {settings.SITE_NAME}!
Contact us: {settings.CONTACT_PHONE}
"""
    send_mail(
        subject,
        full_message,
        settings.CONTACT_EMAIL,
        [to_email],
        fail_silently=True,
    )
