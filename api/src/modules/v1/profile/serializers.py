from rest_framework import serializers
from src.modules.v1.user.serializers import UserSerializer
from src.modules.v1.dictionary.serializers import DictionarySerializer

class ProfileSerializer(serializers.Serializer):
    id = serializers.CharField()
    code = serializers.CharField()
    full_name = serializers.CharField()
    name_alias = serializers.CharField()
    birth_date = serializers.DateField()
    gender = DictionarySerializer()
    avatar = serializers.CharField()
    slug_name = serializers.CharField()
    about_me = serializers.CharField()
    user = UserSerializer()