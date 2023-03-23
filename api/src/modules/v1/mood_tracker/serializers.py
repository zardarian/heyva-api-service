from rest_framework import serializers
from .models import MoodTracker

class MoodTrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoodTracker
        fields = ['id', 'created_at', 'profile_code', 'mood_feel', 'mood_source', 'more', 'mood_value']

class CreateMoodTrackerSerializer(serializers.Serializer):
    mood_feel = serializers.CharField(required=True)
    mood_source = serializers.CharField(required=True)
    more = serializers.CharField(required=False)
    mood_value = serializers.IntegerField(required=False)

class ReadListMoodTrackerSerializer(serializers.Serializer):
    created_start = serializers.DateTimeField(required=False)
    created_end = serializers.DateTimeField(required=False)
    profile_code = serializers.CharField(required=False)
    mood_feel = serializers.CharField(required=False)
    mood_source = serializers.CharField(required=False)
    search = serializers.CharField(required=False)
    mood_value = serializers.IntegerField(required=False)