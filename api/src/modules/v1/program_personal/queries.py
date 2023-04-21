from django.db.models import Q
from .models import ProgramPersonal

def program_personal_not_finished_by_program_id(profile_code, program_id):
    return ProgramPersonal.objects.filter(
        profile_code=profile_code,
        program=program_id,
        deleted_at__isnull=True,
        is_finished=False
    )