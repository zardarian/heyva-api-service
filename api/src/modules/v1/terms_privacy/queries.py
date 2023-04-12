from django.db.models import Q
from datetime import datetime
from .models import TermsPrivacy

def terms_privacy_by_type(type, platform, version):
    terms_privacy = TermsPrivacy.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        type=type
    )

    if platform:
        terms_privacy = terms_privacy.filter(
            platform=platform
        )

    if version:
        terms_privacy = terms_privacy.filter(
            version=version
        )

    return terms_privacy