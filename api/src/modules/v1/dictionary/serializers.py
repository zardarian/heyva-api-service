from rest_framework import serializers
from .models import Dictionary

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'type', 'name', 'parent', 'icon', 'value']

class DictionaryRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'type', 'name', 'parent', 'icon', 'value']

class CreateDictionarySerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    parent = serializers.CharField(required=False)
    icon = serializers.CharField(required=False)
    value = serializers.IntegerField(required=False)

class ReadByTypeDictionarySerializer(serializers.Serializer):
    id = serializers.ListField(required=False, child=serializers.CharField())
    type = serializers.CharField(required=True)
    search = serializers.CharField(required=False)
    name = serializers.ListField(required=False, child=serializers.CharField())
    exclude_onboarding_tags = serializers.BooleanField(required=False)

class UpdateDictionarySerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)
    icon = serializers.CharField(required=False)
    value = serializers.IntegerField(required=False)