from django.conf import settings
from django.core.mail import send_mail

def send_email(subject, message, recipient_list, html_message=None):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
            html_message=html_message,
        )

        return True, 'Successfully send mail'
    except Exception as e:
        return False, str(e)
