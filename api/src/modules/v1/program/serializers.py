from rest_framework import serializers
from datetime import datetime
from src.storages.services import get_object
from src.modules.v1.program_tag.queries import program_tag_by_program_id
from src.modules.v1.program_detail.queries import program_detail_by_program_id
from src.modules.v1.program_personal.queries import program_personal_not_finished_by_program_id
from src.modules.v1.program_tag.serializers import ProgramTagRelationSerializer
from src.modules.v1.program_detail.serializers import ProgramDetailRelationSerializer
from .models import Program
from .queries import program_active_by_parent_id

class ProgramSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()
    program_detail = serializers.SerializerMethodField()
    days_count = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ['id', 'title', 'body', 'banner', 'parent', 'order', 'tags', 'child', 'program_detail', 'days_count']

    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_tags(self, obj):
        tags = program_tag_by_program_id(obj.id)
        return ProgramTagRelationSerializer(tags, many=True).data
    
    def get_child(self, obj):
        child = program_active_by_parent_id(obj.id)
        return ChildProgramSerializer(child, many=True).data
    
    def get_program_detail(self, obj):
        program_detail = program_detail_by_program_id(obj.id)
        return ProgramDetailRelationSerializer(program_detail, many=True).data
    
    def get_days_count(self, obj):
        return None

class ProgramByAuthSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()
    program_detail = serializers.SerializerMethodField()
    days_count = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ['id', 'title', 'body', 'banner', 'parent', 'order', 'tags', 'child', 'program_detail', 'days_count']

    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_tags(self, obj):
        tags = program_tag_by_program_id(obj.id)
        return ProgramTagRelationSerializer(tags, many=True).data
    
    def get_child(self, obj):
        child = program_active_by_parent_id(obj.id)
        return ChildProgramSerializer(child, many=True).data
    
    def get_program_detail(self, obj):
        program_detail = program_detail_by_program_id(obj.id)
        return ProgramDetailRelationSerializer(program_detail, many=True).data
    
    def get_days_count(self, obj):
        program_personal = program_personal_not_finished_by_program_id(obj.id)
        if program_personal:
            program_personal = program_personal.values().first()
            start_date = datetime.combine(program_personal.get('start_date'), datetime.min.time())
            end_date = datetime.combine(program_personal.get('end_date'), datetime.min.time())
            today = datetime.now()
            elapsed_days = (today - start_date).days
            total_days = (end_date - start_date).days

            return "{}/{}".format(elapsed_days, total_days)
        return None
    
class ChildProgramSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    program_detail = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ['id', 'title', 'body', 'banner', 'order', 'program_detail']

    def get_banner(self, obj):
        return get_object(obj.banner)
    
    def get_program_detail(self, obj):
        program_detail = program_detail_by_program_id(obj.id)
        return ProgramDetailRelationSerializer(program_detail, many=True).data

class CreateProgramSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    banner = serializers.FileField(required=False)
    parent = serializers.CharField(required=False)
    order = serializers.IntegerField(required=False)
    tag = serializers.ListField(required=True)

class ReadProgramSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)
