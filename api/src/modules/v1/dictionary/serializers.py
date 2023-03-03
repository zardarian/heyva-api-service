from rest_framework import serializers

class DictionarySerializer(serializers.Serializer):
    id = serializers.CharField()
    type = serializers.CharField()
    name = serializers.CharField()
    parent = serializers.CharField()

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