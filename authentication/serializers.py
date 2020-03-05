from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ReturnedUser:
    username = ""
    first_name = ""
    last_name = ""
    email = ""
    is_admin = ""
    token = ""
    uuid = ""
    is_active = ""

    def __init__(self, username, first_name, last_name, email, is_admin, is_active, token, uuid):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.token = token
        self.uuid = uuid
        self.is_active = is_active


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    uuid = serializers.CharField(read_only=True)
    is_admin = serializers.BooleanField()
    is_active = serializers.BooleanField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists() and self.context['request'] == "post":
            raise serializers.ValidationError("email address already used")
        return value

    def update(self, instance, validated_data):
        # Separate data for users model
        user_data = {
            "username": validated_data.pop('username'),
            "email": validated_data.pop("email"),
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
        }

        # Separate data for profile model
        profile_data = {
            "address": validated_data.pop("address"),
            "resident_country": validated_data.pop("resident_country"),
            "origin_country": validated_data.pop("origin_country"),
            "phone": validated_data.pop("phone"),
            "is_host": validated_data.pop("is_host"),
            "is_admin": validated_data.pop("is_admin"),
            "is_active": validated_data.pop("is_active"),
        }

        instance.username = user_data['username']
        instance.email = user_data['email']
        instance.first_name = user_data['first_name']
        instance.last_name = user_data['last_name']

        instance.save()

        profile = UserProfile.objects.get(user=instance)

        profile.address = profile_data['address']
        profile.resident_country = profile_data['resident_country']
        profile.origin_country = profile_data['origin_country']
        profile.phone = profile_data['phone']
        profile.is_host = profile_data['is_host']
        profile.is_admin = profile.is_admin

        profile.save()
        token = Token.objects.get(user=instance)

        profile_data["uuid"] = profile.uuid
        returned_user = ReturnedUser(**user_data, **profile_data, token=token.key)

        return returned_user

    def create(self, validated_data):
        # Separate data for users model
        user_data = {
            "username": validated_data['email'],
            "email": validated_data.pop("email"),
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
        }

        # Separate data for profile model
        profile_data = {
            "is_admin": validated_data.pop("is_admin"),
            "is_active": validated_data.pop("is_active"),
        }

        user = User.objects.create_user(
            **user_data
        )
        user.set_password(validated_data.pop("password"))
        user.save()

        #  Create token for user
        token = Token.objects.create(
            user=user
        )

        profile = UserProfile.objects.create(
            user=user,
            **profile_data
        )

        profile_data["uuid"] = profile.uuid

        returned_user = ReturnedUser(**user_data, **profile_data, token=token.key)

        return returned_user


class VerifyUserSerializer(serializers.Serializer):
    national_id = serializers.CharField(allow_blank=True)
    passport = serializers.CharField()

    def update(self, instance, validated_data):
        instance.national_id = validated_data['national_id']
        instance.passport = validated_data['passport']

        instance.save()

        return instance

    def create(self, validated_data):
        pass
