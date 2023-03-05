from django.db.models import Q
from datetime import datetime
from .models import Profile

def get_latest_profile_id_today():
    return Profile.objects.filter(
        created_at=datetime.today(),
        deleted_at__isnull=True,
    ).order_by('-code')

def profile_by_code(code):
    return Profile.objects.filter(
        code=code,
        deleted_at__isnull=True,
    )