from rest_framework import serializers
from src.modules.v1.dictionary.serializers import DictionarySerializer
from src.modules.v1.pregnancy.serializers import PregnancyRelationSerializer
from src.modules.v1.interest.serializers import InterestRelationSerializer
from src.modules.v1.pregnancy.queries import pregnancy_by_profile_code
from src.modules.v1.interest.queries import interests_by_profile_code
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    gender = DictionarySerializer()
    pregnancy = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id', 'code', 'full_name', 'name_alias', 'birth_date', 'gender', 'avatar', 'slug_name', 'about_me', 'pregnancy', 'interests']

    def get_pregnancy(self, obj):
        pregnancy = pregnancy_by_profile_code(obj.code).first()
        return PregnancyRelationSerializer(pregnancy).data
    
    def get_interests(self, obj):
        interests = interests_by_profile_code(obj.code)
        return InterestRelationSerializer(interests, many=True).data