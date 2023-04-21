from rest_framework import serializers
from datetime import datetime
from src.helpers import time_of_day
from src.modules.v1.profile.queries import profile_by_user_id
from .models import TrackerDetail
import string

class TrackerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackerDetail
        fields = ['id', 'tracker_type', 'title', 'body', 'content_type', 'json_content', 'order']

class TrackerDetailRelationSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = TrackerDetail
        fields = ['id', 'title', 'body', 'content_type', 'json_content', 'order']

    def get_title(self, obj):
        request = self.context.get('request')
        if request.user.get('id'):
            profile = profile_by_user_id(request.user.get('id')).values().first()
            profile_name = profile.get('full_name')
        else:
            profile_name = "Heyva family"
            
        template = obj.title
        rendered_template = template.replace(
            "{{time_of_day}}", time_of_day(datetime.now().hour)
        ).replace(
            "{{profile_name}}", profile_name
        )
        return rendered_template

class TrackerDetailTitleSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = TrackerDetail
        fields = ['id', 'title', 'order']

    def get_title(self, obj):
        request = self.context.get('request')
        if request.user.get('id'):
            profile = profile_by_user_id(request.user.get('id')).values().first()
            profile_name = profile.get('full_name')
        else:
            profile_name = "Heyva family"
            
        template = obj.title
        rendered_template = template.replace(
            "{{time_of_day}}", time_of_day(datetime.now().hour)
        ).replace(
            "{{profile_name}}", profile_name
        )
        return rendered_template