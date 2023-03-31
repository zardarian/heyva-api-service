from rest_framework import serializers
from src.storages.services import get_object
from .models import ProgramDetail

class ProgramDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramDetail
        fields = ['id', 'program', 'content_type', 'text_content', 'image_content', 'video_content', 'json_content', 'order']

class ProgramDetailRelationSerializer(serializers.ModelSerializer):
    image_content = serializers.SerializerMethodField()
    video_content = serializers.SerializerMethodField()

    class Meta:
        model = ProgramDetail
        fields = ['id', 'content_type', 'text_content', 'image_content', 'video_content', 'json_content', 'order']

    def get_image_content(self, obj):
        return get_object(obj.image_content)
    
    def get_video_content(self, obj):
        return get_object(obj.video_content)
    
class CreateProgramDetailSerializer(serializers.Serializer):
    program = serializers.CharField(required=True)
    content_type = serializers.CharField(required=False)
    text_content = serializers.CharField(required=False)
    image_content = serializers.FileField(required=False)
    video_content = serializers.FileField(required=False)
    json_content = serializers.JSONField(required=False)
    order = serializers.IntegerField(required=False)