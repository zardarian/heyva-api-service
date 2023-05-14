from django.db.models import Q
from .models import ProgramDetail

def program_detail_by_program_id(program_id):
    return ProgramDetail.objects.filter(
        program = program_id,
        deleted_at__isnull=True,
    ).order_by('order')