from django.db.models import Q
from .models import VideoContent

def video_content_active(search, tag):
    video_content = VideoContent.objects.filter(
        is_active=True,
        deleted_at__isnull=True
    )

    if search:
        video_content = video_content.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        )

    if tag:
        video_content = video_content.filter(
            video_content_tag__tag__in=tag
        )
    
    return video_content.distinct('id', 'created_at').order_by('-created_at')

def video_content_by_id(id):
    return VideoContent.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )