from django_q.tasks import async_task
from src.modules.v1.user.models import User
from pusher_push_notifications import PushNotifications
from django.conf import settings

def send_push_notification(user_id):
    # Fetch user and send push notification
    user = User.objects.get(id=user_id)

    # Initialize Pusher Push Notifications client
    beams_client = PushNotifications(
        instance_id=settings.PUSHER_INSTANCE_ID,
        secret_key=settings.PUSHER_PRIMARY_KEY,
    )

    # Prepare notification payload
    notification_payload = {
        'apns': {
            'aps': {
                'alert': {
                    'title': 'New Notification',
                    'body': 'You have a new notification!',
                },
            },
        },
        'fcm': {
            'notification': {
                'title': 'New Notification',
                'body': 'You have a new notification!',
            },
        },
    }

    # Publish the notification to the user's device
    response = beams_client.publish_to_users(
        user_ids=[str(user.device_id)],
        publish_body=notification_payload,
    )

    print(response)

def schedule_daily_notifications():
    users = User.objects.all()
    for user in users:
        async_task(send_push_notification, user.id)