from rest_framework import serializers
from src.storages.services import get_object
from src.modules.v1.doctor_tag.serializers import DoctorTagRelationSerializer
from src.modules.v1.doctor_tag.queries import doctor_tag_by_doctor_id
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'code', 'profile_code', 'name', 'specialist', 'about', 'rate', 'domicile', 'phone_number', 'avatar', 'tags']

    def get_tags(self, obj):
        tags = doctor_tag_by_doctor_id(obj.id)
        return DoctorTagRelationSerializer(tags, many=True).data
    
    def get_avatar(self, obj):
        return get_object(obj.avatar, 3600)

class CreateDoctorSerializer(serializers.Serializer):
    profile_code = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    specialist = serializers.CharField(required=False)
    about = serializers.CharField(required=True)
    rate = serializers.FloatField(required=False)
    domicile = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    avatar = serializers.FileField(required=True)
    tag = serializers.ListField(required=True)

class ReadDoctorSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    tag = serializers.ListField(required=False)
