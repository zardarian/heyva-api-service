from rest_framework import serializers
from src.storages.services import get_object
from src.modules.v1.article_tag.serializers import ArticleTagRelationSerializer
from src.modules.v1.article_tag.queries import article_tag_by_article_id
from src.modules.v1.article_attachment.queries import article_attachment_by_article_id
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    rendered_body = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'tags', 'rendered_body', 'creator', 'banner', 'thumbnail']

    def get_rendered_body(self, obj):
        rendered_body = obj.body
        article_attachments = article_attachment_by_article_id(obj.id)
        
        for article_attachment in article_attachments:
            rendered_body = rendered_body.replace(article_attachment.id, get_object(article_attachment.attachment))
        
        return rendered_body

    def get_tags(self, obj):
        tags = article_tag_by_article_id(obj.id)
        return ArticleTagRelationSerializer(tags, many=True).data
    
    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)
    
class PreviewArticleSerializer(serializers.ModelSerializer):
    rendered_body = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'rendered_body', 'creator', 'banner', 'thumbnail']

    def get_rendered_body(self, obj):
        rendered_body = obj.body
        article_attachments = article_attachment_by_article_id(obj.id)
        
        for article_attachment in article_attachments:
            rendered_body = rendered_body.replace(article_attachment.id, get_object(article_attachment.attachment))
        
        return rendered_body
    
    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_thumbnail(self, obj):
        return get_object(obj.thumbnail)

class CreateArticleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    creator = serializers.CharField(required=True)
    banner = serializers.FileField(required=False)
    thumbnail = serializers.FileField(required=False)
    tag = serializers.ListField(required=True)
    attachment = serializers.ListField(required=False, child=serializers.CharField(required=False))

class ReadSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)
