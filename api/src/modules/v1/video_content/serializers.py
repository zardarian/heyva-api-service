from rest_framework import serializers
from src.storages.services import get_object
from src.modules.v1.video_content_tag.serializers import VideoContentTagRelationSerializer
from src.modules.v1.video_content_attachment.serializers import VideoContentAttachmentRelationSerializer
from src.modules.v1.video_content_tag.queries import video_content_tag_by_video_content_id
from src.modules.v1.video_content_attachment.queries import video_content_attachment_by_video_content_id
from .models import VideoContent

class VideoContentSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = VideoContent
        fields = ['id', 'title', 'body', 'creator', 'tags', 'attachments']

    def get_tags(self, obj):
        tags = video_content_tag_by_video_content_id(obj.id)
        return VideoContentTagRelationSerializer(tags, many=True).data
    
    def get_attachments(self, obj):
        attachments = video_content_attachment_by_video_content_id(obj.id)
        return VideoContentAttachmentRelationSerializer(attachments, many=True).data

class CreateVideoContentSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    creator = serializers.CharField(required=False)
    tag = serializers.ListField(required=True)
    attachment = serializers.ListField(required=False, child=serializers.CharField(required=False))

class ReadVideoContentSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)
