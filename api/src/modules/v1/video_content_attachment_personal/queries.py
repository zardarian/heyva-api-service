from django.db.models import Q
from .models import VideoContentAttachmentPersonal

def video_content_attachment_personal_by_profile_code_and_video_content_id(profile_code, video_content_id, video_content_attachment_id):
    video_content_personal = VideoContentAttachmentPersonal.objects.filter(
        profile_code=profile_code,
        video_content=video_content_id,
        video_content_attachment=video_content_attachment_id,
        deleted_at__isnull=True,
    )

    return video_content_personal

def video_content_attachment_is_finished(profile_code, video_content_id):
    video_content_personal = VideoContentAttachmentPersonal.objects.filter(
        profile_code=profile_code,
        video_content=video_content_id,
        is_finished=True,
        deleted_at__isnull=True,
    )

    return video_content_personal