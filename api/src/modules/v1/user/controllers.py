from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import exceptions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.template.loader import render_to_string
from src.helpers import output_response, generate_registration_url, generate_request_reset_password_url, encrypt, decrypt
from src.constants import RESPONSE_SUCCESS, RESPONSE_ERROR, RESPONSE_FAILED, USER_ALREADY_EXISTS, USER_DOES_NOT_EXISTS, PASSWORD_DOES_NOT_MATCH, MULTIPLE_ROWS_RETURNED, AUTHENTICATION_FAILED, GENDER_FEMALE, ROLE_USER, USER_VERIFICATION_SUCCESS, CONFIRM_PASSWORD_DOES_NOT_MATCH, PAYLOAD_CANNOT_BE_EMPTY, PASSWORD_CANNOT_BE_THE_SAME_AS_PREVIOUS_PASSWORD, USER_IS_NOT_VERIFIED, USER_IS_VERIFIED, CHANNEL_ID_TOKEN_DOES_NOT_MATCH
from src.authentications.basic_auth import CustomBasicAuthentication
from src.authentications.jwt_auth import CustomJWTAuthentication
from src.permissions.admin_permission import IsAdmin
from src.mails.services import send_email
from src.modules.v1.profile.models import Profile
from src.modules.v1.pregnancy.models import Pregnancy
from src.modules.v1.role.models import Role
from src.modules.v1.interest.models import Interest
from src.modules.v1.dictionary.queries import dictionary_by_id
from src.modules.v1.user.queries import user_by_id
from src.modules.v1.profile.queries import get_latest_profile_id_today, profile_by_code, profile_by_user_id
from src.paginations.page_number_pagination import CustomPageNumberPagination
from datetime import datetime
from .serializers import RegisterSerializer, LoginSerializer, LoginResponseSerializer, UserSerializer, RefreshTokenSerializer, ChangePasswordSerializer, RequestResetPasswordSerializer, ResetPasswordSerializer, CheckVerificationSerializer, GoogleLoginSerializer, GoogleRegisterSerializer, GetListSerializer, UserProfileSerializer
from .models import User
from .queries import user_registered, user_registered_not_verified, user_exists, user_by_id, user_exists_verified, user_exists_active, social_user
from django.shortcuts import render
import uuid
import sys

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def register(request):
    payload = RegisterSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        registered_user = user_registered(validated_payload.get('username'), validated_payload.get('email'), validated_payload.get('phone_number'))
        if registered_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_ALREADY_EXISTS, error=None, status_code=400)

        today = datetime.today()
        user_uuid = uuid.uuid4()
        role_uuid = uuid.uuid4()
        profile_uuid = uuid.uuid4()
        pregnancy_uuid = uuid.uuid4()

        user_identifier = validated_payload.get('username', validated_payload.get('email', validated_payload.get('phone_number')))
        encrypted_email = validated_payload.get('email')
        encrypted_phone_number = validated_payload.get('phone_number')

        latest_profile_id = get_latest_profile_id_today()
        if not latest_profile_id:
            profile_code = "{}{}".format(str(today.strftime("%Y%m%d")), str(1).zfill(8))
        else:
            extract_id = int(latest_profile_id.first().code[-8:])
            next_id = extract_id + 1
            profile_code = "{}{}".format(str(today.strftime("%Y%m%d")), str(next_id).zfill(8))
        
        with transaction.atomic():
            unverified_user = user_registered_not_verified(validated_payload.get('username'), validated_payload.get('email'), validated_payload.get('phone_number'))
            if unverified_user:
                user_exists(validated_payload.get('username'), validated_payload.get('email'), validated_payload.get('phone_number')).delete()

            user_payload = {
                'id' : str(user_uuid),
                'created_at' : datetime.now(),
                'created_by' : user_uuid,
                'is_active' : True,
                'username' : validated_payload.get('username'),
                'email' : encrypted_email,
                'phone_number' : encrypted_phone_number,
                'password' : make_password(validated_payload.get('password')),
                'is_verified': False,
            }
            User(**user_payload).save()

            role_payload = {
                'id' : role_uuid,
                'created_at' : datetime.now(),
                'created_by' : user_uuid,
                'user' : user_by_id(str(user_uuid)).first(),
                'role' : dictionary_by_id(ROLE_USER).first(),
            }
            Role(**role_payload).save()

            profile_payload = {
                'id' : str(profile_uuid),
                'created_at' : datetime.now(),
                'created_by' : user_uuid,
                'code' : profile_code,
                'full_name' : validated_payload.get('full_name'),
                'birth_date' : validated_payload.get('birth_date'),
                'gender' : dictionary_by_id(validated_payload.get('gender', GENDER_FEMALE)).first(),
                'user' : user_by_id(str(user_uuid)).first(),
            }
            Profile(**profile_payload).save()

            if validated_payload.get('pregnancy_status') or validated_payload.get('estimated_due_date') or validated_payload.get('child_birth_date'):
                pregnancy_payload = {
                    'id': str(pregnancy_uuid),
                    'created_at' : datetime.now(),
                    'created_by' : user_uuid,
                    'profile_code' : profile_by_code(profile_code).first(),
                    'status' : dictionary_by_id(validated_payload.get('pregnancy_status')).first(),
                    'estimated_due_date' : validated_payload.get('estimated_due_date'),
                    'child_birth_date' : validated_payload.get('child_birth_date'),
                }
                Pregnancy(**pregnancy_payload).save()

            if validated_payload.get('interests'):
                interest_payload = []
                for interest in validated_payload.get('interests'):
                    interest_uuid = uuid.uuid4()
                    payload = Interest(
                        id=interest_uuid,
                        created_at=datetime.now(),
                        created_by=user_uuid,
                        profile_code=profile_by_code(profile_code).first(),
                        interests=dictionary_by_id(interest).first()
                    )
                    interest_payload.append(payload)
                Interest.objects.bulk_create(interest_payload)

            registration_token = CustomJWTAuthentication.create_registration_token(user_payload)
            if validated_payload.get('email'):
                message = render_to_string('user_registration.html', {
                    'page_title': 'Registration',
                    'application_url': settings.APPLICATION_URL,
                    'company_logo': settings.COMPANY_LOGO,
                    'header': 'Registration',
                    'username': user_identifier,
                    'body': 'Hello, We have received your application for registration, click the button below to verify your account.',
                    'verification_link': generate_registration_url(registration_token, user_uuid),
                    'button_name': 'Verify Account',
                    'hardcode_message': 'If you experience problems when clicking the "Verify Account" button, click the URL link below:',
                    'notes': 'Note: This message was sent from an email address that is not monitored. Do not reply to this message. If you have any questions please contact us at',
                    'helper_mail': settings.COMPANY_HELPER_MAIL,
                })
                send_email('User Activation', message, [validated_payload.get('email')], html_message=message)
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': user_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['GET', 'POST'])
def verification(request, id, registration_token):
    try:
        user = user_by_id(id)
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        validate_registration_token = CustomJWTAuthentication.validate_registration_token(registration_token, id)
        if validate_registration_token[0] == False:
            return output_response(success=RESPONSE_FAILED, data=None, message=validate_registration_token[1], error=None, status_code=401)

        with transaction.atomic():
            user.update(
                updated_at=datetime.now(),
                updated_by=id,
                is_verified=True,
            )

        profile = profile_by_user_id(id).first()
        if request.method == 'POST':
            return output_response(success=RESPONSE_SUCCESS, data={'id': id}, message=USER_VERIFICATION_SUCCESS, error=None, status_code=200)
        else:
            return render(request, 'user_verification.html', {
                'page_title': 'Account Verification',
                'application_url': settings.APPLICATION_URL,
                'company_logo': settings.COMPANY_LOGO,
                'header': 'Account Verification',
                'username': profile.full_name,
                'body': 'Hello, Thank you for registering and verifying your account.',
            })
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def login(request):
    payload = LoginSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        existed_user = user_exists_active(validated_payload.get('username'), validated_payload.get('username'), validated_payload.get('username'))
        if not existed_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=401)
        if len(existed_user) > 1:
            return output_response(success=RESPONSE_FAILED, data=None, message=MULTIPLE_ROWS_RETURNED, error=None, status_code=400)
        if existed_user.values().first().get('is_verified') == False:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_IS_NOT_VERIFIED, error=None, status_code=400)

        user = existed_user.values().first()
        password_match = check_password(validated_payload.get('password'), user.get('password'))
        if not password_match:
            return output_response(success=RESPONSE_FAILED, data=None, message=PASSWORD_DOES_NOT_MATCH, error=None, status_code=401)
        
        access_token = CustomJWTAuthentication.create_access_token(user)
        refresh_token = CustomJWTAuthentication.create_refresh_token(user)
        response_data = LoginResponseSerializer(data={
            'id': user.get('id'),
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        if not response_data.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=AUTHENTICATION_FAILED, error=None, status_code=400)

        with transaction.atomic():
            user_update = user_by_id(user.get('id'))
            user_update.update(
                last_login=datetime.now(),
                device_id=validated_payload.get('device_id')
            )

        return output_response(success=RESPONSE_SUCCESS, data=response_data.validated_data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def refresh_token(request):
    payload = RefreshTokenSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        user = user_by_id(validated_payload.get('id'))
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        validate_refresh_token = CustomJWTAuthentication.validate_refresh_token(validated_payload.get('refresh_token'), validated_payload.get('id'))
        if not validate_refresh_token[0]:
            return output_response(success=RESPONSE_FAILED, data=None, message=validate_refresh_token[1], error=None, status_code=400)

        user = user.values().first()
        access_token = CustomJWTAuthentication.create_access_token(user)
        refresh_token = CustomJWTAuthentication.create_refresh_token(user)
        response_data = LoginResponseSerializer(data={
            'id': user.get('id'),
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        if not response_data.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=AUTHENTICATION_FAILED, error=None, status_code=400)

        with transaction.atomic():
            user_update = user_by_id(user.get('id'))
            user_update.update(
                last_login=datetime.now()
            )

        return output_response(success=RESPONSE_SUCCESS, data=response_data.validated_data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def get_user(request):
    try:
        user = user_by_id(request.user.get('id'))
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        user = user.first()
        serialize_user = UserSerializer(user).data

        return output_response(success=RESPONSE_SUCCESS, data=serialize_user, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
def get_list_user(request):
    try:
        payload = GetListSerializer(data=request.query_params)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data

        paginator = CustomPageNumberPagination()
        user = user_registered(validated_payload.get('username'), validated_payload.get('username'), validated_payload.get('username'))
        user = user.order_by('-created_at')
        result_page = paginator.paginate_queryset(user, request)
        serializer = UserProfileSerializer(result_page, many=True)

        return paginator.get_paginated_response(success=RESPONSE_SUCCESS, data=serializer.data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
def change_password(request):
    payload = ChangePasswordSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        user = user_by_id(request.user.get('id'))
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        legacy = user.values().first()
        password_match = check_password(validated_payload.get('old_password'), legacy.get('password'))
        if not password_match:
            return output_response(success=RESPONSE_FAILED, data=None, message=PASSWORD_DOES_NOT_MATCH, error=None, status_code=401)
        
        if validated_payload.get('new_password') != validated_payload.get('confirm_new_password'):
            return output_response(success=RESPONSE_FAILED, data=None, message=CONFIRM_PASSWORD_DOES_NOT_MATCH, error=None, status_code=401)
        
        user.update(
            updated_at=datetime.now(),
            updated_by=request.user.get('id'),
            password=make_password(validated_payload.get('new_password'))
        )

        return output_response(success=RESPONSE_SUCCESS, data={'id': legacy.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def request_reset_password(request):
    try:
        payload = RequestResetPasswordSerializer(data=request.data)
        if not payload.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
        
        validated_payload = payload.validated_data
        if not validated_payload.get('email') and not validated_payload.get('phone_number'):
            return output_response(success=RESPONSE_FAILED, data=None, message=PAYLOAD_CANNOT_BE_EMPTY, error=None, status_code=400)

        user = user_exists(username=None, email=validated_payload.get('email'), phone_number=validated_payload.get('phone_number'))
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)

        user = user.values().first()
        request_reset_password_token = CustomJWTAuthentication.create_request_reset_password_token(user)
        if validated_payload.get('email'):
            message = render_to_string('request_reset_password.html', {
                'page_title': 'Request Reset Password',
                'application_url': settings.APPLICATION_URL,
                'company_logo': settings.COMPANY_LOGO,
                'header': 'Request Reset Password',
                'username': validated_payload.get('email'),
                'body': 'Hello, We have received your request to reset password, click the button below to reset your password.',
                'verification_link': generate_request_reset_password_url(request_reset_password_token, user.get('id')),
                'button_name': 'Reset Password',
                'hardcode_message': 'If you experience problems when clicking the "Reset Password" button, click the URL link below:',
                'notes': 'Note: This message was sent from an email address that is not monitored. Do not reply to this message. If you have any questions please contact us at',
                'helper_mail': settings.COMPANY_HELPER_MAIL,
            })
            send_email('Reset Password', message, [validated_payload.get('email')], html_message=message)

        return output_response(success=RESPONSE_SUCCESS, data={'id': user.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['PUT'])
@authentication_classes([CustomBasicAuthentication])
def reset_password(request, id, reset_password_token):
    payload = ResetPasswordSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        user = user_by_id(id)
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)

        validate_request_reset_password_token = CustomJWTAuthentication.validate_request_reset_password_token(reset_password_token, id)
        if validate_request_reset_password_token[0] == False:
            return output_response(success=RESPONSE_FAILED, data=None, message=validate_request_reset_password_token[1], error=None, status_code=401)
        
        legacy = user.values().first()
        password_match = check_password(validated_payload.get('new_password'), legacy.get('password'))
        if password_match:
            return output_response(success=RESPONSE_FAILED, data=None, message=PASSWORD_CANNOT_BE_THE_SAME_AS_PREVIOUS_PASSWORD, error=None, status_code=401)
        
        if validated_payload.get('new_password') != validated_payload.get('confirm_new_password'):
            return output_response(success=RESPONSE_FAILED, data=None, message=CONFIRM_PASSWORD_DOES_NOT_MATCH, error=None, status_code=401)
        
        user.update(
            updated_at=datetime.now(),
            updated_by=request.user.get('id'),
            password=make_password(validated_payload.get('new_password'))
        )

        return output_response(success=RESPONSE_SUCCESS, data={'id': legacy.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def check_verification(request):
    payload = CheckVerificationSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data

    try:
        existed_user = user_exists_active(validated_payload.get('username'), validated_payload.get('username'), validated_payload.get('username'))
        if not existed_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=401)
        if len(existed_user) > 1:
            return output_response(success=RESPONSE_FAILED, data=None, message=MULTIPLE_ROWS_RETURNED, error=None, status_code=400)
        if existed_user.values().first().get('is_verified') == False:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_IS_NOT_VERIFIED, error=None, status_code=400)

        return output_response(success=RESPONSE_SUCCESS, data=None, message=USER_IS_VERIFIED, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def google_register(request):
    payload = GoogleRegisterSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        existed_user = social_user(validated_payload.get('email'), 'google')
        if existed_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_ALREADY_EXISTS, error=None, status_code=400)

        registered_user = user_registered(None, validated_payload.get('email'), None)
        if registered_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_ALREADY_EXISTS, error=None, status_code=400)
        
        today = datetime.today()
        user_uuid = uuid.uuid4()
        role_uuid = uuid.uuid4()
        profile_uuid = uuid.uuid4()
        pregnancy_uuid = uuid.uuid4()

        encrypted_email = validated_payload.get('email')

        latest_profile_id = get_latest_profile_id_today()
        if not latest_profile_id:
            profile_code = "{}{}".format(str(today.strftime("%Y%m%d")), str(1).zfill(8))
        else:
            extract_id = int(latest_profile_id.first().code[-8:])
            next_id = extract_id + 1
            profile_code = "{}{}".format(str(today.strftime("%Y%m%d")), str(next_id).zfill(8))

        with transaction.atomic():
            unverified_user = user_registered_not_verified(None, validated_payload.get('email'), None)
            if unverified_user:
                user_exists(None, validated_payload.get('email'), None).delete()

            user_payload = {
                'id' : str(user_uuid),
                'created_at' : datetime.now(),
                'created_by' : user_uuid,
                'is_active' : True,
                'email' : encrypted_email,
                'is_verified': False,
                'channel': 'google',
                'channel_id_token': validated_payload.get('google_id'),
                'device_id': validated_payload.get('device_id'),
            }
            User(**user_payload).save()

            role_payload = {
                'id' : role_uuid,
                'created_at' : datetime.now(),
                'created_by' : user_uuid,
                'user' : user_by_id(str(user_uuid)).first(),
                'role' : dictionary_by_id(ROLE_USER).first(),
            }
            Role(**role_payload).save()

            profile_payload = {
                'id' : str(profile_uuid),
                'created_at' : datetime.now(),
                'created_by' : user_uuid,
                'code' : profile_code,
                'full_name' : validated_payload.get('full_name'),
                'birth_date' : validated_payload.get('birth_date'),
                'gender' : dictionary_by_id(validated_payload.get('gender', GENDER_FEMALE)).first(),
                'avatar': validated_payload.get('avatar'),
                'user' : user_by_id(str(user_uuid)).first(),
            }
            Profile(**profile_payload).save()

            if validated_payload.get('pregnancy_status') or validated_payload.get('estimated_due_date') or validated_payload.get('child_birth_date'):
                pregnancy_payload = {
                    'id': str(pregnancy_uuid),
                    'created_at' : datetime.now(),
                    'created_by' : user_uuid,
                    'profile_code' : profile_by_code(profile_code).first(),
                    'status' : dictionary_by_id(validated_payload.get('pregnancy_status')).first(),
                    'estimated_due_date' : validated_payload.get('estimated_due_date'),
                    'child_birth_date' : validated_payload.get('child_birth_date'),
                }
                Pregnancy(**pregnancy_payload).save()

            if validated_payload.get('interests'):
                interest_payload = []
                for interest in validated_payload.get('interests'):
                    interest_uuid = uuid.uuid4()
                    payload = Interest(
                        id=interest_uuid,
                        created_at=datetime.now(),
                        created_by=user_uuid,
                        profile_code=profile_by_code(profile_code).first(),
                        interests=dictionary_by_id(interest).first()
                    )
                    interest_payload.append(payload)
                Interest.objects.bulk_create(interest_payload)

        registration_token = CustomJWTAuthentication.create_registration_token(user_payload)
        if validated_payload.get('email'):
            message = render_to_string('user_registration.html', {
                'page_title': 'Registration',
                'application_url': settings.APPLICATION_URL,
                'company_logo': settings.COMPANY_LOGO,
                'header': 'Registration',
                'username': validated_payload.get('email'),
                'body': 'Hello, We have received your application for registration, click the button below to verify your account.',
                'verification_link': generate_registration_url(registration_token, user_uuid),
                'button_name': 'Verify Account',
                'hardcode_message': 'If you experience problems when clicking the "Verify Account" button, click the URL link below:',
                'notes': 'Note: This message was sent from an email address that is not monitored. Do not reply to this message. If you have any questions please contact us at',
                'helper_mail': settings.COMPANY_HELPER_MAIL,
            })
            send_email('User Activation', message, [validated_payload.get('email')], html_message=message)
        
        return output_response(success=RESPONSE_SUCCESS, data={'id': user_payload.get('id')}, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)

@api_view(['POST'])
@authentication_classes([CustomBasicAuthentication])
def google_login(request):
    payload = GoogleLoginSerializer(data=request.data)
    if not payload.is_valid():
        return output_response(success=RESPONSE_FAILED, data=None, message=None, error=payload.errors, status_code=400)
    
    validated_payload = payload.validated_data
    try:
        existed_user = social_user(validated_payload.get('email'), 'google')
        if not existed_user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=401)

        user = existed_user.values().first()
        if validated_payload.get('google_id') != user.get('channel_id_token'):
            return output_response(success=RESPONSE_FAILED, data=None, message=CHANNEL_ID_TOKEN_DOES_NOT_MATCH, error=None, status_code=401)
        
        access_token = CustomJWTAuthentication.create_access_token(user)
        refresh_token = CustomJWTAuthentication.create_refresh_token(user)
        response_data = LoginResponseSerializer(data={
            'id': user.get('id'),
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        if not response_data.is_valid():
            return output_response(success=RESPONSE_FAILED, data=None, message=AUTHENTICATION_FAILED, error=None, status_code=400)

        with transaction.atomic():
            user_update = user_by_id(user.get('id'))
            user_update.update(
                last_login=datetime.now(),
                device_id=validated_payload.get('device_id')
            )

        return output_response(success=RESPONSE_SUCCESS, data=response_data.validated_data, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)
    
@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAdmin])
def delete(request):
    try:
        user = user_by_id(request.user.get('id'))
        if not user:
            return output_response(success=RESPONSE_FAILED, data=None, message=USER_DOES_NOT_EXISTS, error=None, status_code=404)
        
        user = user.first().delete()

        return output_response(success=RESPONSE_SUCCESS, data=None, message=None, error=None, status_code=200)
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error_message = "{}:{}".format(filename, line_number)
        return output_response(success=RESPONSE_ERROR, data=None, message=error_message, error=str(e), status_code=500)