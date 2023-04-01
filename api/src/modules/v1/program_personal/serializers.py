from rest_framework import serializers
from .models import ProgramPersonal

class ProgramPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramPersonal
        fields = ['id', 'profile_code', 'program', 'is_finished', 'start_date', 'end_date']

class CreateProgramPersonalSerializer(serializers.Serializer):
    program = serializers.CharField(required=True)

class UpdateProgramPersonalSerializer(serializers.Serializer):
    is_finished = serializers.BooleanField(required=True)