from celery import Celery
from celery.schedules import crontab
from celery import shared_task
from celery.utils.log import get_task_logger
from src.modules.v1.notification.models import Notification
from src.modules.v1.program_personal.queries import program_personal_unfinished_by_date
from src.constants import SCHEDULER_USER, PROGRAM_BREATHING, PROGRAM_PELVIC
from datetime import datetime
import uuid

app = Celery()
logger = get_task_logger(__name__)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     print('anjing')
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#     print('asu')
#     app.conf.beat_schedule = {
#         # Executes every Monday morning at 7:30 a.m.
#         'add-every-minute': {
#             'task': 'tasks.add',
#             'schedule': crontab(minute='*/1'),
#             'args': (16, 16),
#         },
#     }
#     # Calls test('hello') every 30 seconds.
#     # It uses the same signature of previous task, an explicit name is
#     # defined to avoid this task replacing the previous one defined.
#     sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

@shared_task
def send_notification_program_reminder():
    logger.info('send_notification_program_reminder started')
    registered_personal_breathing = program_personal_unfinished_by_date(PROGRAM_BREATHING, datetime.now())
    registered_personal_pelvic = program_personal_unfinished_by_date(PROGRAM_PELVIC, datetime.now())
    
    print(registered_personal_breathing)
    print(registered_personal_pelvic)
    for registered_breathing in registered_personal_breathing:
        print('asu3')
        print(registered_breathing.profile_code)
        # send_one_notification.delay(registered_breathing.get('profile_code'), 'test', 'test')
    logger.info('send_notification_program_reminder finished')

@shared_task
def send_one_notification(profile_code, title, body):
    notification_payload = {
        'id' : uuid.uuid4(),
        'created_at' : datetime.now(),
        'created_by' : SCHEDULER_USER,
        'updated_at' : datetime.now(),
        'updated_by' : SCHEDULER_USER,
        'deleted_at' : None,
        'deleted_by' : None,
        'title' : title,
        'body' : body,
        'profile_code' : profile_code,
        'is_read' : False
    }
    Notification(**notification_payload).save()