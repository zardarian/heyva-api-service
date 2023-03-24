from django.db.models import Q
from .models import VideoContentTag

def video_content_tag_by_video_content_id(video_content_id):
    return VideoContentTag.objects.filter(
        video_content = video_content_id,
        deleted_at__isnull=True,
    )