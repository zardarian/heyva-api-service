from rest_framework import serializers
from src.modules.v1.tracker_detail.queries import tracker_detail_by_id
from src.modules.v1.tracker_detail.serializers import TrackerDetailTitleSerializer
from .models import TrackerDaily

class TrackerDailySerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()

    class Meta:
        model = TrackerDaily
        fields = ['id', 'profile_code', 'type', 'response']

    def get_response(self, obj):
        response = []
        for resp in obj.response:
            tracker_detail = tracker_detail_by_id(resp.get('tracker_detail_id')).first()
            tracker_detail_serializer = TrackerDetailTitleSerializer(tracker_detail).data
            answer = tracker_detail.json_content.get(resp.get('answer'))
            
            response.append({'tracker_detail': tracker_detail_serializer, 'answer': answer})

        return response

class CreateTrackerDailySerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    response = serializers.JSONField(required=True)

class ReadListSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    date = serializers.DateField(required=True)