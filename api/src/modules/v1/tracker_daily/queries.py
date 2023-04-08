from django.db.models import Q
from datetime import datetime
from .models import TrackerDaily

def tracker_daily_today_by_profile_code(profile_code):
    return TrackerDaily.objects.filter(
        created_at__date=datetime.today(),
        deleted_at__isnull=True,
        profile_code=profile_code
    )

def tracker_daily_insight(profile_code, type, date):
    tracker_daily = TrackerDaily.objects.filter(
        created_at__date=date,
        deleted_at__isnull=True,
        profile_code=profile_code
    )

    if type:
        tracker_daily = tracker_daily.filter(
            type=type
        )

    return tracker_daily

def tracker_daily_recommendation(profile_code, date):
    return TrackerDaily.objects.filter(
        created_at__date=date,
        deleted_at__isnull=True,
        profile_code=profile_code
    )