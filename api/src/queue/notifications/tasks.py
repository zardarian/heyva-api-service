from django_q.tasks import async_task, schedule
from src.modules.v1.user.models import User
from src.modules.v1.profile.models import Profile
from pusher_push_notifications import PushNotifications
from django.conf import settings

print('a1')

def send_push_notification(user_id):
    # Fetch user and send push notification
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user_id=user_id)
    print(profile)

    # # Initialize Pusher Push Notifications client
    # beams_client = PushNotifications(
    #     instance_id=settings.PUSHER_INSTANCE_ID,
    #     secret_key=settings.PUSHER_PRIMARY_KEY,
    # )

    # # Prepare notification payload
    # notification_payload = {
    #     'apns': {
    #         'aps': {
    #             'alert': {
    #                 'title': 'New Notification',
    #                 'body': 'You have a new notification!',
    #             },
    #         },
    #     },
    #     'fcm': {
    #         'notification': {
    #             'title': 'New Notification',
    #             'body': 'You have a new notification!',
    #         },
    #     },
    # }

    # # Publish the notification to the user's device
    # response = beams_client.publish_to_users(
    #     user_ids=[str(user.device_id)],
    #     publish_body=notification_payload,
    # )

    print("{} {}".format("Notification sent to", user.email))

def schedule_daily_notifications():
    print('anjing')
    # users = User.objects.all()
    users = User.objects.filter(email='kang-bakso@harakirimail.com')
    print(users)
    for user in users:
        async_task(send_push_notification, user.id)
    
    return "Successfully schedule daily notifications"

schedule(schedule_daily_notifications, schedule_type='I', minutes=1)