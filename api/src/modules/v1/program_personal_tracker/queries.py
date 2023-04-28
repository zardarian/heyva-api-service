from django.db.models import Q
from .models import ProgramPersonalTracker

def program_personal_tracker_not_finished_by_program_id(profile_code, program_id):
    return ProgramPersonalTracker.objects.filter(
        Q(program=program_id) | Q(child_program=program_id),
        profile_code=profile_code,
        deleted_at__isnull=True,
        is_finished=False
    )

def program_personal_tracker_finished_by_program_id(profile_code, program_id):
    return ProgramPersonalTracker.objects.filter(
        Q(program=program_id) | Q(child_program=program_id),
        profile_code=profile_code,
        deleted_at__isnull=True,
        is_finished=True
    )

def program_personal_tracker_finished_by_program_id_date(profile_code, program_id, check_in_date):
    return ProgramPersonalTracker.objects.filter(
        Q(program=program_id) | Q(child_program=program_id),
        profile_code=profile_code,
        deleted_at__isnull=True,
        is_finished=True,
        check_in_date=check_in_date
    )

def program_personal_tracker_by_program_child_date(profile_code, program_id, child_program_id, check_in_date):
    program_personal_tracker = ProgramPersonalTracker.objects.filter(
        profile_code=profile_code,
        program=program_id,
        deleted_at__isnull=True,
    )

    if child_program_id:
        program_personal_tracker = program_personal_tracker.filter(child_program=program_id)

    if check_in_date:
        program_personal_tracker = program_personal_tracker.filter(check_in_date=check_in_date)

    return program_personal_tracker