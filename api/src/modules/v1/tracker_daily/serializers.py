from rest_framework import serializers
from src.modules.v1.tracker_detail.queries import tracker_detail_by_id
from src.modules.v1.tracker_detail.serializers import TrackerDetailTitleSerializer
from src.modules.v1.tracker_type.serializers import TrackerTypeRelationSerializer
from .models import TrackerDaily

class TrackerDailySerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()
    type = TrackerTypeRelationSerializer()

    class Meta:
        model = TrackerDaily
        fields = ['id', 'profile_code', 'type', 'response']

    def get_response(self, obj):
        request = self.context.get('request')
        response = []
        for resp in obj.response:
            tracker_detail = tracker_detail_by_id(resp.get('tracker_detail_id')).first()
            tracker_detail_serializer = TrackerDetailTitleSerializer(tracker_detail, context={'request': request}).data
            
            if resp.get('answer'):
                answer = list(filter(lambda item: item['id'] in resp.get('answer'), tracker_detail.json_content))
            else:
                answer = []
            
            response.append({'tracker_detail': tracker_detail_serializer, 'answer': answer, 'note': resp.get('note')})

        return response

class CreateTrackerDailySerializer(serializers.Serializer):
    data = serializers.JSONField(required=True)

class InsightSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    date = serializers.ListField(required=True, child=serializers.DateField())

class RecommendationSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)