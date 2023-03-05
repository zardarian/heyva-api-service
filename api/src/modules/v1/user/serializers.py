from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    is_verified = serializers.BooleanField()
    last_login = serializers.DateTimeField()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, max_length=15)
    password = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    pregnancy_status = serializers.CharField(required=True)
    interests = serializers.CharField(required=True)
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