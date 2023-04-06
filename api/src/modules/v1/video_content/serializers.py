from rest_framework import serializers
from src.storages.services import get_object
from src.modules.v1.video_content_tag.serializers import VideoContentTagRelationSerializer
from src.modules.v1.video_content_attachment.serializers import VideoContentAttachmentRelationSerializer, VideoContentAttachmentRelationByAuthSerializer
from src.modules.v1.video_content_personal.serializers import VideoContentPersonalRelationSerializer
from src.modules.v1.video_content_tag.queries import video_content_tag_by_video_content_id
from src.modules.v1.video_content_attachment.queries import video_content_attachment_by_video_content_id
from src.modules.v1.video_content_personal.queries import video_content_personal_by_profile_code_and_video_content_id
from .models import VideoContent

class VideoContentSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = VideoContent
        fields = ['id', 'title', 'body', 'creator', 'tags', 'attachments', 'banner', 'thumbnail']

    def get_tags(self, obj):
        tags = video_content_tag_by_video_content_id(obj.id)
        return VideoContentTagRelationSerializer(tags, many=True).data
    
    def get_attachments(self, obj):
        attachments = video_content_attachment_by_video_content_id(obj.id)
        return VideoContentAttachmentRelationSerializer(attachments, many=True).data
    
    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)

class PreviewVideoContentSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = VideoContent
        fields = ['id', 'title', 'body', 'creator', 'banner', 'thumbnail']
    
    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)
    
class VideoContentByAuthSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    is_finished = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = VideoContent
        fields = ['id', 'title', 'body', 'creator', 'tags', 'attachments', 'is_finished', 'banner', 'thumbnail']

    def get_tags(self, obj):
        tags = video_content_tag_by_video_content_id(obj.id)
        return VideoContentTagRelationSerializer(tags, many=True).data
    
    def get_attachments(self, obj):
        request = self.context.get('request')
        attachments = video_content_attachment_by_video_content_id(obj.id)
        return VideoContentAttachmentRelationByAuthSerializer(attachments, context={'request': request}, many=True).data
    
    def get_is_finished(self, obj):
        request = self.context.get('request')
        video_content_personal = video_content_personal_by_profile_code_and_video_content_id(request.user.get('profile_code'), obj.id).first()
        return VideoContentPersonalRelationSerializer(video_content_personal).data
    
    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)

class CreateVideoContentSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    creator = serializers.CharField(required=False)
    tag = serializers.ListField(required=True)
    attachment = serializers.ListField(required=False, child=serializers.CharField(required=False))
    banner = serializers.FileField(required=True)
    thumbnail = serializers.FileField(required=True)

class ReadVideoContentSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)
