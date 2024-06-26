from rest_framework import serializers
from src.modules.v1.role.serializers import RoleRelationSerializer
from src.modules.v1.role.queries import role_by_user_id
from src.modules.v1.profile.queries import profile_by_user_id
from src.storages.services import get_object
from .models import User

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_verified', 'last_login', 'roles']

    def get_roles(self, obj):
        roles = role_by_user_id(obj.id)
        return RoleRelationSerializer(roles, many=True).data
    
class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_verified', 'last_login', 'profile', 'avatar']

    def get_profile(self, obj):
        profile = profile_by_user_id(obj.id)
        return profile.values('code', 'full_name', 'avatar').first()
    
    def get_avatar(self, obj):
        profile = self.get_profile(obj)
        if not profile.get('avatar'):
            return None
        
        if 'http' in profile.get('avatar'):
            return profile.get('avatar')
        
        return get_object(profile.get('avatar'), 3600)
    
class UserRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_verified', 'last_login']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, max_length=15)
    password = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    pregnancy_status = serializers.CharField(required=False)
    interests = serializers.ListField(required=False, child=serializers.CharField(required=False))
    estimated_due_date = serializers.DateField(required=False)
    child_birth_date = serializers.DateField(required=False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    device_id = serializers.CharField(required=False)

class RefreshTokenSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    refresh_token = serializers.CharField(required=True)

class LoginResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class AuthenticateSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    is_verified = serializers.BooleanField(required=False)
    last_login = serializers.DateTimeField(required=False)
    profile_code = serializers.CharField(required=False)
    roles = serializers.ListField(required=False, child=serializers.CharField(required=False))
    is_bearer = serializers.BooleanField(required=False)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

class CheckVerificationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

class GoogleRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    google_id = serializers.CharField(required=True)
    avatar = serializers.CharField(required=True)
    device_id = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    pregnancy_status = serializers.CharField(required=False)
    interests = serializers.ListField(required=False, child=serializers.CharField(required=False))
    estimated_due_date = serializers.DateField(required=False)
    child_birth_date = serializers.DateField(required=False)

class GoogleLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    google_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=False)

class GetListSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)