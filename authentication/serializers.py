from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField("username", queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type:password'}, write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):

        # First, add the user
        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])

        # Second, create the profile
        user_profile = UserProfile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.save()
        user_profile.save()

        return user

    def update(self, instance, validated_data):
        user = instance
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.set_password(validated_data['password'])

        user_profile = UserProfile.objects.get(user=user)
        user_profile.first_name = validated_data['first_name']
        user_profile.last_name = validated_data['last_name']
        user.save()

        user_profile.save()
        return user

