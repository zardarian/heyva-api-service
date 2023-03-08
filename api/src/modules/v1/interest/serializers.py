from rest_framework import serializers
from .models import Interest
from src.modules.v1.dictionary.serializers import DictionaryRelationSerializer

class InterestSerializer(serializers.ModelSerializer):
    interests = DictionaryRelationSerializer()
    
    class Meta:
        model = Interest
        fields = ['id', 'profile_code', 'interests']

class InterestRelationSerializer(serializers.ModelSerializer):
    interests = DictionaryRelationSerializer()

    class Meta:
        model = Interest
        fields = ['id', 'interests']
