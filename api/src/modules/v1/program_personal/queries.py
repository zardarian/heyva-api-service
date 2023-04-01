from django.db.models import Q
from .models import ProgramPersonal

def program_personal_not_finished_by_program_id(program_id):
    return ProgramPersonal.objects.filter(
        program=program_id,
        deleted_at__isnull=True,
        is_finished=False
    )