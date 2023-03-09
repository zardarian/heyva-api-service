from rest_framework import serializers
from src.storages.services import get_object
from .models import ArticleAttachment

class ArticleAttachmentSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = ArticleAttachment
        fields = ['id', 'article', 'attachment']

    def get_attachment(self, obj):
        return get_object(obj.attachment)

class ArticleAttachmentRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleAttachment
        fields = ['id', 'attachment']

class CreateArticleAttachmentSerializer(serializers.Serializer):
    article = serializers.CharField(required=False)
    attachment = serializers.ListField(required=True, child=serializers.FileField())