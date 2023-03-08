from rest_framework import serializers
from .models import Dictionary

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'type', 'name', 'parent']

class DictionaryRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'type', 'name', 'parent']

class CreateDictionarySerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    parent = serializers.CharField(required=False)

class ReadByTypeDictionarySerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    name = serializers.CharField(required=False)

class UpdateDictionarySerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)