from rest_framework import serializers
from src.storages.services import get_object
from src.modules.v1.video_content_attachment_personal.serializers import VideoContentAttachmentPersonalRelationSerializer
from src.modules.v1.video_content_attachment_personal.queries import video_content_attachment_personal_by_profile_code_and_video_content_id
from .models import VideoContentAttachment

class VideoContentAttachmentSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = VideoContentAttachment
        fields = ['id', 'video_content', 'attachment_order', 'attachment', 'attachment_title', 'attachment_length', 'thumbnail']

    def get_attachment(self, obj):
        return get_object(obj.attachment)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)

class VideoContentAttachmentRelationSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = VideoContentAttachment
        fields = ['id', 'attachment_order', 'attachment', 'attachment_title', 'attachment_length', 'thumbnail']

    def get_attachment(self, obj):
        return get_object(obj.attachment)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)
    
class VideoContentAttachmentRelationByAuthSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    is_finished = serializers.SerializerMethodField()

    class Meta:
        model = VideoContentAttachment
        fields = ['id', 'attachment_order', 'attachment', 'attachment_title', 'attachment_length', 'is_finished', 'thumbnail']

    def get_attachment(self, obj):
        return get_object(obj.attachment)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)
    
    def get_is_finished(self, obj):
        request = self.context.get('request')
        video_content_attachment_personal = video_content_attachment_personal_by_profile_code_and_video_content_id(request.user.get('profile_code'), obj.video_content, obj.id).first()
        return VideoContentAttachmentPersonalRelationSerializer(video_content_attachment_personal).data

class CreateVideoContentAttachmentSerializer(serializers.Serializer):
    video_content = serializers.CharField(required=False)
    attachment = serializers.ListField(required=True, child=serializers.FileField())
    attachment_title = serializers.ListField(required=True, child=serializers.CharField())
    thumbnail = serializers.ListField(required=True, child=serializers.FileField())