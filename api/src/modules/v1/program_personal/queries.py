from django.db.models import Q
from .models import ProgramPersonal
from datetime import datetime

def program_personal_not_finished_by_program_id(profile_code, program_id):
    return ProgramPersonal.objects.filter(
        Q(is_finished=False) | Q(end_date__gt=datetime.now()),
        profile_code=profile_code,
        program=program_id,
        deleted_at__isnull=True
    )

def program_personal_unfinished_by_date(program_id, check_in_date):
    return ProgramPersonal.objects.filter(
        Q(is_finished=False) | Q(end_date__gt=datetime.now()),
        program=program_id,
        deleted_at__isnull=True
    ).extra(
        tables=['program_personal_tracker'],
        where=[
            '''
                not (program_personal_tracker.profile_code = program_personal.profile_code
                and program_personal_tracker.program_id = program_personal.program_id
                and program_personal_tracker.is_finished = true
                and program_personal_tracker.check_in_date = %s)
                and program_personal_tracker.check_in_date = %s
            '''
        ],
        params=[
            check_in_date, check_in_date
        ]
    )
