import django
from django.conf import settings
from django.db import transaction, IntegrityError

# Django 1.5 add support for custom auth user model
AUTH_USER_MODEL = settings.AUTH_USER_MODEL

atomic = transaction.atomic
