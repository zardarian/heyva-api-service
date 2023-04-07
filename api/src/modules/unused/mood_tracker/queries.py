from django.db.models import Q
from .models import MoodTracker

def mood_tracker_list(created_start, created_end, profile_code, mood_feel, mood_source, search):
    mood_tracker = MoodTracker.objects.filter(
        deleted_at__isnull=True
    )

    if created_start and created_end:
        mood_tracker = mood_tracker.filter(
            created_at__range=(created_start, created_end)
        )

    if profile_code:
        mood_tracker = mood_tracker.filter(
            profile_code=profile_code
        )

    if mood_feel:
        mood_tracker = mood_tracker.filter(
            mood_feel=mood_feel
        )

    if mood_source:
        mood_tracker = mood_tracker.filter(
            mood_source=mood_source
        )

    if search:
        mood_tracker = mood_tracker.filter(
            profile_code__full_name__icontains=search
        )
    
    return mood_tracker.order_by('-created_at')