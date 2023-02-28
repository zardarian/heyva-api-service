from django.db.models import Q
from .models import User

def user_exists(username, email, phone_number):
    return User.objects.filter(
        Q(username=username) | Q(email=email) | Q(phone_number=phone_number),
        is_active=True,
        deleted_at__isnull=True
    )

def user_by_id(id):
    return User.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True
    )