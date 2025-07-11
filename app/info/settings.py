from django.conf import settings

ADMIN_EMAIL = getattr(settings, "ADMIN_EMAIL_ADDRESS", "admin@giftshop.com")
CONTACT_EMAIL = getattr(settings, "CONTACT_EMAIL_ADDRESS", "admin@giftshop.com")
