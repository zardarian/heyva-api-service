from rest_framework import serializers
from src.modules.v1.dictionary.serializers import DictionaryRelationSerializer
from .models import ArticleTag

class ArticleTagSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = ArticleTag
        fields = ['id', 'article', 'tag']

class ArticleTagRelationSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = ArticleTag
        fields = ['id', 'tag']