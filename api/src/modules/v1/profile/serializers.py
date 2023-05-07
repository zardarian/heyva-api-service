from rest_framework import serializers
from src.storages.services import get_object
from src.modules.v1.dictionary.serializers import DictionarySerializer
from src.modules.v1.pregnancy.serializers import PregnancyRelationSerializer
from src.modules.v1.interest.serializers import InterestRelationSerializer
from src.modules.v1.user.serializers import UserRelationSerializer
from src.modules.v1.pregnancy.queries import pregnancy_by_profile_code
from src.modules.v1.interest.queries import interests_by_profile_code
from src.modules.v1.user.queries import user_by_id
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    gender = DictionarySerializer()
    avatar = serializers.SerializerMethodField()
    pregnancy = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    user = UserRelationSerializer()
    class Meta:
        model = Profile
        fields = ['id', 'code', 'full_name', 'name_alias', 'birth_date', 'gender', 'avatar', 'slug_name', 'about_me', 'pregnancy', 'interests', 'user']

    def get_avatar(self, obj):
        if not obj.avatar:
            return None
        
        if 'http' in obj.avatar:
            return obj.avatar
        
        return get_object(obj.avatar, 3600)

    def get_pregnancy(self, obj):
        pregnancy = pregnancy_by_profile_code(obj.code).first()
        return PregnancyRelationSerializer(pregnancy).data
    
    def get_interests(self, obj):
        interests = interests_by_profile_code(obj.code)
        return InterestRelationSerializer(interests, many=True).data
    
class UpdateProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    name_alias = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    avatar = serializers.FileField(required=False)
    slug_name = serializers.CharField(required=False)
    about_me = serializers.CharField(required=False)
    pregnancy_status = serializers.CharField(required=False)
    interests = serializers.ListField(required=False, child=serializers.CharField(required=False))
    estimated_due_date = serializers.DateField(required=False)
    child_birth_date = serializers.DateField(required=False)