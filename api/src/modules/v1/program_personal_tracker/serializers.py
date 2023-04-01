from rest_framework import serializers
from .models import ProgramPersonalTracker

class ProgramPersonalTrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgramPersonalTracker
        fields = ['id', 'program', 'child_program', 'profile_code', 'is_finished', 'check_in_date']

class CreateProgramPersonalTrackerSerializer(serializers.Serializer):
    program = serializers.CharField(required=True)
    child_program = serializers.CharField(required=False)

class UpdateProgramPersonalTrackerSerializer(serializers.Serializer):
    is_finished = serializers.BooleanField(required=True)