from rest_framework import serializers
from .models import Program

class ProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Program
        fields = ['id', 'title', 'body', 'banner', 'parent']

class CreateProgramSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    parent = serializers.CharField(required=False)
    banner = serializers.FileField(required=False)
    tag = serializers.ListField(required=True)