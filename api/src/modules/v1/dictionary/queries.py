from django.db.models import Q
from .models import Dictionary

def dictionary_active_by_type(type, search):
    dictionary = Dictionary.objects.filter(
        type=type,
        is_active=True,
        deleted_at__isnull=True
    )

    if search:
        dictionary = dictionary.filter(
            name__icontains=search
        )
    
    return dictionary

def dictionary_active_by_type_id(type, id, search):
    dictionary = Dictionary.objects.filter(
        type=type,
        is_active=True,
        deleted_at__isnull=True
    )

    if id:
        dictionary = dictionary.filter(
            id__in = id
        )

    if search:
        dictionary = dictionary.filter(
            name__icontains=search
        )
    
    return dictionary

def dictionary_by_id(id):
    return Dictionary.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )

def dictionary_active_by_multiple_id(ids):
    return Dictionary.objects.filter(
        id__in=ids,
        is_active=True,
        deleted_at__isnull=True,
    )