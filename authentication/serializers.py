from rest_framework import serializers
from .models import UserProfile, PinVerify, PaymentMethod
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
    # profile_image = ""

    def __init__(
            self,
            username,
            first_name,
            last_name,
            email,
            is_admin,
            is_active,
            token,
            uuid):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.token = token
        self.uuid = uuid
        # self.profile_image = profile_image
        self.is_active = is_active


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    # profile_image = serializers.CharField(read_only=True, allow_blank=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    uuid = serializers.CharField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists(
        ) and self.context['request'] == "post":
            raise serializers.ValidationError("email address already used")
        return value

    def update(self, instance, validated_data):
        # Separate data for users model
        user_data = {
            # "username": validated_data.pop('username'),
            # "email": validated_data.pop("email"),
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
        }

        # Separate data for profile model
        profile_data = {
            # "address": validated_data.pop("address"),
            # "resident_country": validated_data.pop("resident_country"),
            # "origin_country": validated_data.pop("origin_country"),
            "phone": validated_data.pop("phone"),
            # "is_host": validated_data.pop("is_host"),
            # "is_admin": validated_data.pop("is_admin"),
            # "is_active": validated_data.pop("is_active"),
        }

        instance.phone = profile_data['phone']
        # instance.email = user_data['email']
        instance.save()

        user = instance.user

        # profile.address = profile_data['address']
        # profile.resident_country = profile_data['resident_country']
        # profile.origin_country = profile_data['origin_country']
        # profile.phone = profile_data['phone']
        # profile.is_host = profile_data['is_host']
        # profile.is_admin = profile.is_admin
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']

        user.save()
        token = Token.objects.get(user=user)

        profile_data["uuid"] = instance.uuid
        returned_user = ReturnedUser(
            **user_data, **profile_data, token=token.key)

        return returned_user

    def create(self, validated_data):
        # Separate data for users model
        try:
            pin_code = self.context['pin_code']
        except:
            pin_code = "12345"

        user_data = {
            "username": validated_data['email'],
            "email": validated_data.pop("email"),
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
        }

        # Separate data for profile model
        profile_data = {
            "is_admin": False,
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

        PinVerify.objects.create(user=profile, pin=pin_code)

        profile_data["uuid"] = profile.uuid

        returned_user = ReturnedUser(
            **user_data, **profile_data, token=token.key)

        return returned_user


class VerifyUserSerializer(serializers.Serializer):
    national_id = serializers.CharField(allow_blank=True)
    passport = serializers.CharField(allow_blank=True)

    def update(self, instance, validated_data):
        instance.national_id = validated_data['national_id']
        instance.passport = validated_data['passport']
        instance.verification_status = "P"

        instance.save()

        return instance

    def create(self, validated_data):
        pass


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class UserProfileSerializerWithDetails(serializers.ModelSerializer):
    user = UserRegisterSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'
