from rest_framework import serializers
from src.constants import CONTENT_ARTICLE, CONTENT_VIDEO, CONTENT_PROGRAM
from src.modules.v1.dictionary.queries import dictionary_by_id
from src.modules.v1.article.queries import article_by_id
from src.modules.v1.video_content.queries import video_content_by_id
from src.modules.v1.program.queries import program_by_id
from src.modules.v1.article.serializers import PreviewArticleSerializer, ArticleSerializer
from src.modules.v1.video_content.serializers import PreviewVideoContentSerializer, VideoContentSerializer
from src.modules.v1.program.serializers import PreviewProgramSerializer, ProgramSerializer
from .models import Content

class ContentSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'content_reference_id', 'content_type', 'contents']

    def get_contents(self, obj):
        if obj.content_type.id == CONTENT_ARTICLE:
            content = article_by_id(obj.content_reference_id).first()
            return ArticleSerializer(content).data
        elif obj.content_type.id == CONTENT_VIDEO:
            content = video_content_by_id(obj.content_reference_id).first()
            return VideoContentSerializer(content).data
        elif obj.content_type.id == CONTENT_PROGRAM:
            content = program_by_id(obj.content_reference_id).first()
            return ProgramSerializer(content).data

class PreviewContentSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'content_reference_id', 'content_type', 'contents']

    def get_contents(self, obj):
        if obj.content_type.id == CONTENT_ARTICLE:
            content = article_by_id(obj.content_reference_id).first()
            return PreviewArticleSerializer(content).data
        elif obj.content_type.id == CONTENT_VIDEO:
            content = video_content_by_id(obj.content_reference_id).first()
            return PreviewVideoContentSerializer(content).data
        elif obj.content_type.id == CONTENT_PROGRAM:
            content = program_by_id(obj.content_reference_id).first()
            return PreviewProgramSerializer(content).data

class ReadListContentSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    tag = serializers.ListField(required=False, child=serializers.CharField())