from django.db.models import Q
from .models import Program

def program_by_id(id):
    return Program.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )

def program_active_parent(search, tag):
    program = Program.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        parent__isnull=True
    )

    if search:
        program = program.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        )

    if tag:
        program = program.filter(
            program_tag__tag__in=tag
        )
    
    return program.distinct('id', 'created_at').order_by('-created_at')

def program_active_by_parent_id(parent_id):
    program = Program.objects.filter(
        is_active=True,
        deleted_at__isnull=True,
        parent=parent_id
    )
    
    return program.order_by('order')
