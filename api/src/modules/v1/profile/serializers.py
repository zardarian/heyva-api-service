from rest_framework import serializers
from src.modules.v1.dictionary.serializers import DictionarySerializer
from src.modules.v1.user.serializers import UserSerializer
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    gender = DictionarySerializer()
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['id', 'code', 'full_name', 'name_alias', 'birth_date', 'gender', 'avatar', 'slug_name', 'about_me', 'user']
