from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class ReturnedUser:
    username = ""
    first_name = ""
    last_name = ""
    email = ""
    address = ""
    resident_country = ""
    origin_country = ""
    phone = ""
    is_host = ""
    is_admin = ""
    token = ""

    def __init__(self, username,  first_name, last_name, email, address, resident_country, origin_country, phone, is_host, is_admin, token):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.resident_country = resident_country
        self.origin_country = origin_country
        self.phone = phone
        self.is_host = is_host
        self.is_admin = is_admin
        self.token = token


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    address = serializers.CharField()
    resident_country = serializers.CharField()
    origin_country = serializers.CharField()
    phone = serializers.CharField()
    token = serializers.CharField(read_only=True)

    # These information will be handled by a different serializer to verify documents

    # national_id = serializers.FileField()
    # passport = serializers.FileField()
    is_host = serializers.BooleanField()
    is_admin = serializers.BooleanField()

    #  Validate username for duplicates etc
    def validate_username(self, value):
        request_method = self.context["request"]
        if request_method == "put":
            is_exits = User.objects.filter(username=value)
            if is_exits.exists():
                return value
            else:
                raise serializers.ValidationError("username does not exits")

        elif request_method == "post":
            is_exits = User.objects.filter(username=value)
            if is_exits.exists():
                raise serializers.ValidationError("username already exits")
            return value
        else:
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
        returned_user = ReturnedUser(**user_data, **profile_data, token=token.key)

        return returned_user

    def create(self, validated_data):
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
        }

        user = User.objects.create_user(
            **user_data
        )
        user.set_password(validated_data.pop("password"))

        #  Create token for user
        token = Token.objects.create(
            user=user
        )

        UserProfile.objects.create(
            user=user,
            **profile_data
        )

        # user_to_return = CustomUser("hello", "hi")

        returned_user = ReturnedUser(** user_data, **profile_data, token=token.key)

        return returned_user




