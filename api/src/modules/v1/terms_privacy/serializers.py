from rest_framework import serializers
from .models import TermsPrivacy

class TermsPrivacySerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsPrivacy
        fields = ['id', 'is_active', 'type', 'platform', 'version', 'text_content', 'json_content']

class ReadTermsPrivacyByTypeSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    platform = serializers.CharField(required=False)
    version = serializers.CharField(required=False)
