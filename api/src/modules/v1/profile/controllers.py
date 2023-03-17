from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, authentication_classes
from src.helpers import output_response, encrypt, decrypt
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, USER_DOES_NOT_EXISTS
from src.authentications.jwt_auth import CustomJWTAuthentication
from datetime import datetime
from .serializers import ProfileSerializer
from .models import Profile
from .queries import profile_by_user_id
import sys

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def get_profile(request):
    try:
        profile = profile_by_user_id(request.user.get('id'))
        if not profile:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        profile = profile.first()
        serialize_user = ProfileSerializer(profile).data

        return output_response(success=RESPONSE_SUCCESS, data=serialize_user, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)