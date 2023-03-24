from django.db.models import Q
from .models import VideoContentPersonal

def video_content_personal_by_profile_code_and_video_content_id(profile_code, video_content_id):
    video_content_personal = VideoContentPersonal.objects.filter(
        profile_code=profile_code,
        video_content=video_content_id,
        deleted_at__isnull=True,
    )

    return video_content_personal