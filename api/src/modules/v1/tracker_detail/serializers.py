from rest_framework import serializers
from .models import TrackerDetail

class TrackerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackerDetail
        fields = ['id', 'tracker_type', 'title', 'body', 'content_type', 'json_content', 'order']

class TrackerDetailRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackerDetail
        fields = ['id', 'title', 'body', 'content_type', 'json_content', 'order']

class TrackerDetailTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackerDetail
        fields = ['id', 'title', 'order']