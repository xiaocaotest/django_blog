from rest_framework import serializers

from .models import UserInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = [
            "id",
            "nick_name",
        ]


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = [
            "id",
            "username",
            "password",
            "nick_name",
            "email",
            "is_superuser",
        ]

    def create(self, validated_data):
        """密码加密保存"""
        user = super(RegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user