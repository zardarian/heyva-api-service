from django.db.models import Q
from .models import TrackerDetail

def tracker_detail_by_id(id):
    return TrackerDetail.objects.filter(
        id=id,
        deleted_at__isnull=True
    )

def tracker_detail_by_tracker_type_id(tracker_type_id):
    return TrackerDetail.objects.filter(
        deleted_at__isnull=True,
        tracker_type=tracker_type_id
    ).order_by('order')