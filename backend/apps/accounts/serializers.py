from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name", "password", "password_confirm", "role")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Mật khẩu xác nhận không trùng khớp."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    remaining_quota = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name", "role", "prediction_quota", "used_quota", "remaining_quota", "avatar_url")
        read_only_fields = ("id", "prediction_quota", "used_quota", "remaining_quota")

    def get_remaining_quota(self, obj) -> int:
        return max(0, obj.prediction_quota - obj.used_quota)