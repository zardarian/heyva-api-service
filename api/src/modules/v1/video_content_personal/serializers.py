from rest_framework import serializers
from .models import VideoContentPersonal

class VideoContentPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoContentPersonal
        fields = ['id', 'profile_code', 'video_content', 'is_finished']

class VideoContentPersonalRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoContentPersonal
        fields = ['id', 'profile_code', 'is_finished']

class CreateVideoContentPersonalSerializer(serializers.Serializer):
    video_content = serializers.CharField(required=True)
    is_finished = serializers.BooleanField(required=True)