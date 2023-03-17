from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, SUCCESSFULLY_UPDATE, FAILED_UPDATE
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.super_admin_permission import IsSuperAdmin
from src.modules.v1.user.queries import user_by_id
from src.modules.v1.dictionary.queries import dictionary_by_id
from datetime import datetime
from .serializers import UpdateRoleSerializer
from .models import Role
from .queries import role_by_user_id
import uuid
import sys

@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsSuperAdmin])
def update(request, user_id):
    payload = UpdateRoleSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=FAILED_UPDATE, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        with transaction.atomic():
            insert_payload = []
            role_by_user_id(user_id).delete()

            for role in validated_payload.get('roles'):
                role_uuid = uuid.uuid4()
                payload = Role(
                    id = role_uuid,
                    created_at = datetime.now(),
                    created_by = request.user.get('id'),
                    updated_at = datetime.now(),
                    updated_by = request.user.get('id'),
                    user = user_by_id(user_id).first(),
                    role = dictionary_by_id(role).first()
                )
                insert_payload.append(payload)
            Role.objects.bulk_create(insert_payload)
        
        return output_response(success=RESPONSE_SUCCESS, data=None, message=SUCCESSFULLY_UPDATE, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)