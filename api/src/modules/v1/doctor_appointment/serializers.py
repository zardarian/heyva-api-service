from rest_framework import serializers
from .models import DoctorAppointment

class DoctorAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAppointment
        fields = ['id', 'profile_code', 'doctor_code', 'date', 'hour', 'service']

class CreateDoctorAppointmentSerializer(serializers.Serializer):
    doctor_code = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    hour = serializers.TimeField(required=True)
    service = serializers.CharField(required=True)
