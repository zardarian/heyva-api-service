from rest_framework import serializers
from src.modules.v1.dictionary.serializers import DictionaryRelationSerializer
from .models import ProgramTag

class ProgramTagSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = ProgramTag
        fields = ['id', 'program', 'tag']

class ProgramTagRelationSerializer(serializers.ModelSerializer):
    tag = DictionaryRelationSerializer()

    class Meta:
        model = ProgramTag
        fields = ['id', 'tag']