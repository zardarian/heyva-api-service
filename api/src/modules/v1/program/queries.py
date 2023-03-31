from django.db.models import Q
from .models import Program

def program_by_id(id):
    return Program.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )