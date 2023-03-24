from django.db.models import Q
from .models import VideoContentAttachment

def video_content_attachment_unused():
    video_content_attachment = VideoContentAttachment.objects.filter(
        video_content__isnull=True,
        deleted_at__isnull=True,
    )
    
    return video_content_attachment.order_by('-created_at')

def video_content_attachment_by_id(id):
    video_content_attachment = VideoContentAttachment.objects.filter(
        id=id
    )
    
    return video_content_attachment

def video_content_attachment_by_multiple_id(ids):
    video_content_attachment = VideoContentAttachment.objects.filter(
        id__in=ids
    )
    
    return video_content_attachment.order_by('-created_at')

def video_content_attachment_by_video_content_id(video_content_id):
    return VideoContentAttachment.objects.filter(
        video_content=video_content_id,
        deleted_at__isnull=True,
    ).order_by('attachment_order')