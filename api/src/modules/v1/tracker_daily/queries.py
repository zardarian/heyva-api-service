from django.db.models import Q
from datetime import datetime
from .models import TrackerDaily

def tracker_daily_today_by_profile_code(profile_code):
    return TrackerDaily.objects.filter(
        created_at__date=datetime.today(),
        deleted_at__isnull=True,
        profile_code=profile_code
    )

def tracker_daily_by_profile_code_and_date(profile_code, date):
    return TrackerDaily.objects.filter(
        created_at__date=date,
        deleted_at__isnull=True,
        profile_code=profile_code
    )