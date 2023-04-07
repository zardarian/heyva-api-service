from django.db.models import Q
from .models import TrackerType

def tracker_type_by_id(id):
    return TrackerType.objects.filter(
        id=id,
        deleted_at__isnull=True
    )

def tracker_type_active(type):
    tracker_type = TrackerType.objects.filter(
        deleted_at__isnull=True,
    )

    if type:
        tracker_type = tracker_type.filter(
            type=type
        )

    return tracker_type