from rest_framework import serializers
from src.modules.v1.tracker_detail.queries import tracker_detail_by_tracker_type_id
from src.modules.v1.tracker_detail.serializers import TrackerDetailRelationSerializer
from .models import TrackerType

class TrackerTypeSerializer(serializers.ModelSerializer):
    tracker_detail = serializers.SerializerMethodField()

    class Meta:
        model = TrackerType
        fields = ['id', 'type', 'title', 'description', 'tracker_detail']

    def get_tracker_detail(self, obj):
        request = self.context.get('request')
        tracker_detail = tracker_detail_by_tracker_type_id(obj.id)
        return TrackerDetailRelationSerializer(tracker_detail, context={'request': request}, many=True).data
    
class TrackerTypeRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackerType
        fields = ['id', 'type', 'title', 'description']

class ReadTrackerTypeSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)