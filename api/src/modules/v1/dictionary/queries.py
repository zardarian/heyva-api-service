from django.db.models import Q
from .models import Dictionary
from src.constants import EXCLUDED_ONBOARDING_TAG_ID

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

def dictionary_active_by_type_id(type, id, search, name, exclude_onboarding_tags):
    dictionary = Dictionary.objects.filter(
        type=type,
        is_active=True,
        deleted_at__isnull=True
    )

    if id:
        dictionary = dictionary.filter(
            id__in = id
        )

    if name:
        dictionary = dictionary.filter(
            name__in = name
        )

    if exclude_onboarding_tags:
        dictionary = dictionary.filter(
            ~Q(id__in = EXCLUDED_ONBOARDING_TAG_ID)
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