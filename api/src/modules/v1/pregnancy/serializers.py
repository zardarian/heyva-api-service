from rest_framework import serializers
from .models import Pregnancy
from src.modules.v1.dictionary.serializers import DictionaryRelationSerializer

class PregnancySerializer(serializers.ModelSerializer):
    status = DictionaryRelationSerializer()
    
    class Meta:
        model = Pregnancy
        fields = ['id', 'profile_code', 'status', 'estimated_due_date', 'child_birth_date']

class PregnancyRelationSerializer(serializers.ModelSerializer):
    status = DictionaryRelationSerializer()
    
    class Meta:
        model = Pregnancy
        fields = ['id', 'status', 'estimated_due_date', 'child_birth_date']