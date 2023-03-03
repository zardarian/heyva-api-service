from django.db.models import Q
from .models import Dictionary

def get_active_by_type(type, search):
    dictionary = Dictionary.objects.filter(
        type=type
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