from django.db.models import Q
from .models import User

def user_exists(username, email, phone_number):
    user_exist = User.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
    )

    if username:
        return user_exist.filter(
            username=username,
        )
    if email:
        return user_exist.filter(
            email=email,
        )
    if phone_number:
        return user_exist.filter(
            phone_number=phone_number,
        )

def user_exists_verified(username, email, phone_number):
    user_exist = User.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        is_verified=True,
    )
    
    if username:
        return user_exist.filter(
            username=username,
        )
    if email:
        return user_exist.filter(
            email=email,
        )
    if phone_number:
        return user_exist.filter(
            phone_number=phone_number,
        )

def user_by_id(id):
    return User.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )