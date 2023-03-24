from rest_framework import serializers
from .models import VideoContentAttachmentPersonal

class VideoContentAttachmentPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoContentAttachmentPersonal
        fields = ['id', 'profile_code', 'video_content', 'video_content_attachment', 'is_finished']

class VideoContentAttachmentPersonalRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoContentAttachmentPersonal
        fields = ['id', 'profile_code', 'video_content', 'video_content_attachment', 'is_finished']

class CreateVideoContentAttachmentPersonalSerializer(serializers.Serializer):
    video_content = serializers.CharField(required=True)
    video_content_attachment = serializers.CharField(required=True)
    is_finished = serializers.BooleanField(required=True)