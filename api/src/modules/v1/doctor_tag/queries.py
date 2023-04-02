from django.db.models import Q
from .models import DoctorTag

def doctor_tag_by_doctor_id(doctor_id):
    return DoctorTag.objects.filter(
        doctor=doctor_id,
        deleted_at__isnull=True,
    )