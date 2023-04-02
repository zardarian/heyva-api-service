from rest_framework import serializers
from src.modules.v1.dictionary.serializers import DictionaryRelationSerializer
from .models import DoctorTag

class DoctorTagSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = DoctorTag
        fields = ['id', 'doctor', 'tag']

class DoctorTagRelationSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = DoctorTag
        fields = ['id', 'tag']