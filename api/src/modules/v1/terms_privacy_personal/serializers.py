from rest_framework import serializers
from .models import TermsPrivacyPersonal

class TermsPrivacyPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsPrivacyPersonal
        fields = ['id', 'profile_code', 'terms_privacy', 'is_agree']

class CreateTermsPrivacyPersonalSerializer(serializers.Serializer):
    terms_privacy = serializers.CharField(required=True)
    is_agree = serializers.BooleanField(required=True)

class CreateTermsPrivacyPersonalListSerializer(serializers.Serializer):
    terms_privacy = serializers.ListField(required=True, child=serializers.CharField())
    is_agree = serializers.ListField(required=True, child=serializers.BooleanField())

class ReadTermsPrivacyPersonalByTypeSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)