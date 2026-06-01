from django.conf import settings


def site_settings(request):
    return {
        'contact_phone': settings.CONTACT_PHONE,
        'contact_whatsapp': settings.CONTACT_WHATSAPP,
        'contact_email': settings.CONTACT_EMAIL,
        'site_name': 'BIN SAEED OUTLET',
    }
