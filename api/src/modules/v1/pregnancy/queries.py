from .models import Pregnancy

def pregnancy_by_profile_code(profile_code):
    return Pregnancy.objects.filter(
        profile_code=profile_code,
        deleted_at__isnull=True,
    )