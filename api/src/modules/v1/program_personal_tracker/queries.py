from django.db.models import Q
from .models import ProgramPersonalTracker

def program_personal_tracker_not_finished_by_program_id(program_id):
    return ProgramPersonalTracker.objects.filter(
        Q(program=program_id) | Q(child_program=program_id),
        deleted_at__isnull=True,
        is_finished=False
    )