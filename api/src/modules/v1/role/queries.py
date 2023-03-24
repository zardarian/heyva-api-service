from .models import Role

def role_by_user_id(user_id):
    return Role.objects.filter(
        user=user_id,
        deleted_at__isnull=True,
    )