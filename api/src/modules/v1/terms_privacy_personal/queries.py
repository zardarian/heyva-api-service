from django.db.models import Q
from datetime import datetime
from .models import TermsPrivacyPersonal

def terms_privacy_personal_by_terms_privacy_id(profile_code, terms_privacy_id):
    return TermsPrivacyPersonal.objects.filter(
        deleted_at__isnull=True,
        profile_code=profile_code,
        terms_privacy_id=terms_privacy_id,
        is_agree=True
    )
