from rest_framework import serializers
from .models import Role
from src.modules.v1.dictionary.serializers import DictionaryRelationSerializer

class RoleSerializer(serializers.ModelSerializer):
    role = DictionaryRelationSerializer()
    
    class Meta:
        model = Role
        fields = ['id', 'user', 'role']

class RoleRelationSerializer(serializers.ModelSerializer):
    role = DictionaryRelationSerializer()
    
    class Meta:
        model = Role
        fields = ['id', 'role']