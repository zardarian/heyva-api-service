from rest_framework import serializers

class ProfileSerializer(serializers.Serializer):
    id = serializers.CharField()
    code = serializers.CharField()
    full_name = serializers.CharField()
    name_alias = serializers.CharField()
    birth_date = serializers.DateField()
    gender = serializers.CharField()
    avatar = serializers.CharField()
    slug_name = serializers.CharField()
    about_me = serializers.CharField()