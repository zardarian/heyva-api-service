from rest_framework import serializers
from src.modules.v1.article_tag.serializers import ArticleTagRelationSerializer
from src.modules.v1.article_tag.queries import article_tag_by_article_id
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'tags']

    def get_tags(self, obj):
        tags = article_tag_by_article_id(obj.id)
        return ArticleTagRelationSerializer(tags, many=True).data

class CreateArticleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    tag = serializers.ListField(required=True)

class ReadSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)
