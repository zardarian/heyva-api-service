from django.db.models import Q
from .models import User

def user_registered(username, email, phone_number):
    user_exist = User.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        is_verified=True
    )

    if username:
        user_exist = user_exist.filter(
            username=username,
        )
    if email:
        user_exist = user_exist.filter(
            email=email,
        )
    if phone_number:
        user_exist = user_exist.filter(
            phone_number=phone_number,
        )
        
    return user_exist

def user_registered_not_verified(username, email, phone_number):
    user_exist = User.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        is_verified=False
    )

    if username:
        user_exist = user_exist.filter(
            username=username,
        )
    if email:
        user_exist = user_exist.filter(
            email=email,
        )
    if phone_number:
        user_exist = user_exist.filter(
            phone_number=phone_number,
        )
        
    return user_exist

def user_exists(username, email, phone_number):
    user_exist = User.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
    )

    if username:
        user_exist = user_exist.filter(
            username=username,
        )
    if email:
        user_exist = user_exist.filter(
            email=email,
        )
    if phone_number:
        user_exist = user_exist.filter(
            phone_number=phone_number,
        )
        
    return user_exist

def user_exists_active(username, email, phone_number):
    return User.objects.filter(
        Q(username=username) | Q(email=email) | Q(phone_number=phone_number),
        is_active=True,
        deleted_at__isnull=True,
    )

def user_exists_verified(username, email, phone_number):
    return User.objects.filter(
        Q(username=username) | Q(email=email) | Q(phone_number=phone_number),
        is_active=True,
        deleted_at__isnull=True,
        is_verified=True,
    )

def user_exists_not_verified(username, email, phone_number):
    return User.objects.filter(
        Q(username=username) | Q(email=email) | Q(phone_number=phone_number),
        is_active=True,
        deleted_at__isnull=True,
        is_verified=False,
    )

def user_by_id(id):
    return User.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )