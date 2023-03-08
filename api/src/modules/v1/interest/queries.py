from .models import Interest

def interests_by_profile_code(profile_code):
    return Interest.objects.filter(
        profile_code=profile_code,
        deleted_at__isnull=True,
    )