from rest_framework import serializers
from src.modules.v1.terms_privacy_personal.queries import terms_privacy_personal_by_terms_privacy_id
from .models import TermsPrivacy

class TermsPrivacySerializer(serializers.ModelSerializer):
    is_agree = serializers.SerializerMethodField()

    class Meta:
        model = TermsPrivacy
        fields = ['id', 'is_active', 'type', 'platform', 'version', 'text_content', 'json_content', 'is_agree']

    def get_is_agree(self, obj):
        request = self.context.get('request')
        if not request.user.get('profile_code'):
            return False
        else:
            terms_privacy_personal = terms_privacy_personal_by_terms_privacy_id(request.user.get('profile_code'), obj.id)

            if not terms_privacy_personal:
                return False
            return terms_privacy_personal.values().first().get('is_agree')

class ReadTermsPrivacyByTypeSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    platform = serializers.CharField(required=False)
    version = serializers.CharField(required=False)

class ReadListSerializer(serializers.Serializer):
    type = serializers.ListField(required=False)
    platform = serializers.CharField(required=False)
    version = serializers.CharField(required=False)
