from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from src.paginations.page_number_pagination import CustomPageNumberPagination
from src.helpers import output_response
from src.storages.services import put_object, remove_object
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND, CONTENT_PROGRAM
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from datetime import datetime
from .serializers import ReadTrackerTypeSerializer, TrackerTypeSerializer
from .models import TrackerType
from .queries import tracker_type_active
import uuid
import sys

@api_view(['GET'])
@authentication_classes([CustomBasicAuthentication])
def read_list(request):
    try:
        payload = ReadTrackerTypeSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        tracker_type = tracker_type_active(validated_payload.get('type'))
        serializer = TrackerTypeSerializer(tracker_type, many=True).data

        return output_response(success=RESPONSE_SUCCESS, data=serializer, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)