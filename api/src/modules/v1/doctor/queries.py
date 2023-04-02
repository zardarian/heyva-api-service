from django.db.models import Q
from datetime import datetime
from .models import Doctor

def get_latest_doctor_code_today():
    return Doctor.objects.filter(
        created_at__date=datetime.today(),
        deleted_at__isnull=True,
    ).order_by('-code')

def doctor_by_id(id):
    return Doctor.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )

def doctor_active(search, tag):
    doctor = Doctor.objects.filter(
        is_active=True,
        deleted_at__isnull=True
    )

    if search:
        doctor = doctor.filter(
            Q(name__icontains=search) | Q(about__icontains=search)
        )

    if tag:
        doctor = doctor.filter(
            doctor_tag__tag__in=tag
        )
    
    return doctor.distinct('id', 'created_at').order_by('-created_at')