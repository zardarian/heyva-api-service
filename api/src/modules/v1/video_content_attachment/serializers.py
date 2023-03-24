from rest_framework import serializers
from src.storages.services import get_object
from .models import VideoContentAttachment

class VideoContentAttachmentSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = VideoContentAttachment
        fields = ['id', 'video_content', 'attachment_order', 'attachment', 'attachment_title', 'attachment_length']

    def get_attachment(self, obj):
        return get_object(obj.attachment)

class VideoContentAttachmentRelationSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = VideoContentAttachment
        fields = ['id', 'attachment_order', 'attachment', 'attachment_title', 'attachment_length']

    def get_attachment(self, obj):
        return get_object(obj.attachment)

class CreateVideoContentAttachmentSerializer(serializers.Serializer):
    video_content = serializers.CharField(required=False)
    attachment = serializers.ListField(required=True, child=serializers.FileField())
    attachment_title = serializers.ListField(required=True, child=serializers.CharField())