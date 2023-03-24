from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes
from datetime import datetime
from src.helpers import output_response
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, OBJECTS_NOT_FOUND
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.modules.v1.video_content_personal.models import VideoContentPersonal
from src.modules.v1.profile.queries import profile_by_code
from src.modules.v1.video_content.queries import video_content_by_id
from src.modules.v1.video_content_attachment.queries import video_content_attachment_by_id, video_content_attachment_by_video_content_id
from src.modules.v1.video_content_personal.queries import video_content_personal_by_profile_code_and_video_content_id
from .serializers import CreateVideoContentAttachmentPersonalSerializer
from .models import VideoContentAttachmentPersonal
from .queries import video_content_attachment_personal_by_profile_code_and_video_content_id, video_content_attachment_is_finished
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
def create(request):
    payload = CreateVideoContentAttachmentPersonalSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        video_content_attachment_personal_uuid = uuid.uuid4()

        with transaction.atomic():
            video_content_attachment_personal = video_content_attachment_personal_by_profile_code_and_video_content_id(request.user.get('profile_code'), validated_payload.get('video_content'), validated_payload.get('video_content_attachment'))
            if video_content_attachment_personal:
                video_content_attachment_personal.update(
                    is_finished=validated_payload.get('is_finished')
                )
                video_content_attachment_personal_uuid = video_content_attachment_personal.values().first().get('id')
            else:
                video_content_attachment_personal_payload = {
                    'id' : video_content_attachment_personal_uuid,
                    'created_at' : datetime.now(),
                    'created_by' : request.user.get('id'),
                    'profile_code' : profile_by_code(request.user.get('profile_code')).first(),
                    'video_content' : video_content_by_id(validated_payload.get('video_content')).first(),
                    'video_content_attachment' : video_content_attachment_by_id(validated_payload.get('video_content_attachment')).first(),
                    'is_finished' : validated_payload.get('is_finished'),
                }
                VideoContentAttachmentPersonal(**video_content_attachment_personal_payload).save()

            video_content_personal = video_content_personal_by_profile_code_and_video_content_id(request.user.get('profile_code'), validated_payload.get('video_content'))
            if not video_content_personal:
                video_content_personal_uuid = uuid.uuid4()
                video_content_personal_payload = {
                    'id' : video_content_personal_uuid,
                    'created_at' : datetime.now(),
                    'created_by' : request.user.get('id'),
                    'profile_code' : profile_by_code(request.user.get('profile_code')).first(),
                    'video_content' : video_content_by_id(validated_payload.get('video_content')).first(),
                    'is_finished' : validated_payload.get('is_finished'),
                }
                VideoContentPersonal(**video_content_personal_payload).save()

            video_content_personal_attachment_finished = video_content_attachment_is_finished(request.user.get('profile_code'), validated_payload.get('video_content'))
            video_content_attachments = video_content_attachment_by_video_content_id(validated_payload.get('video_content'))
            
            if len(video_content_personal_attachment_finished) == len(video_content_attachments):
                video_content_personal.update(
                    is_finished=True
                )
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': video_content_attachment_personal_uuid}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)