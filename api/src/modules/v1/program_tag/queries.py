from django.db.models import Q
from .models import ProgramTag

def program_tag_by_program_id(program_id):
    return ProgramTag.objects.filter(
        program = program_id,
        deleted_at__isnull=True,
    )