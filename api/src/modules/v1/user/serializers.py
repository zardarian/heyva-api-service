from rest_framework import serializers
from src.modules.v1.role.serializers import RoleRelationSerializer
from src.modules.v1.role.queries import role_by_user_id
from .models import User

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_verified', 'last_login', 'roles']

    def get_roles(self, obj):
        roles = role_by_user_id(obj.id)
        return RoleRelationSerializer(roles, many=True).data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, max_length=15)
    password = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    pregnancy_status = serializers.CharField(required=True)
    interests = serializers.ListField(required=True, child=serializers.CharField(required=True))
    estimated_due_date = serializers.DateField(required=False)
    child_birth_date = serializers.DateField(required=False)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class RefreshTokenSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    refresh_token = serializers.CharField(required=True)

class LoginResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class AuthenticateSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    is_verified = serializers.BooleanField()
    last_login = serializers.DateTimeField()
    profile_code = serializers.CharField()
    roles = serializers.ListField(child=serializers.CharField())