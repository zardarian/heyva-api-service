from rest_framework import serializers
from src.modules.v1.dictionary.serializers import DictionaryRelationSerializer
from .models import VideoContentTag

class VideoContentTagSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = VideoContentTag
        fields = ['id', 'video_content', 'tag']

class VideoContentTagRelationSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = VideoContentTag
        fields = ['id', 'tag']