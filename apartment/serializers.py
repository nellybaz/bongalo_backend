from apartment.models import Apartment, Review
from rest_framework import serializers
from authentication.models import UserProfile
from .models import Category
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Category
        fields = ["category"]


class ApartmentSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    title = serializers.CharField()
    owner = serializers.CharField()
    main_image = serializers.CharField()
    description = serializers.CharField()
    available_rooms = serializers.IntegerField()
    country = serializers.CharField()
    number_of_bathrooms = serializers.IntegerField()
    price = serializers.IntegerField()
    discount = serializers.FloatField()
    type = serializers.CharField()
    amenities = serializers.CharField()
    rules = serializers.CharField()
    is_active = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    check_in = serializers.DateTimeField()
    check_out = serializers.DateTimeField()

    def validate_owner(self, value):
        _owner_ = UserProfile.objects.filter(uuid=value)
        if _owner_.exists():
            return value
        raise serializers.ValidationError("user does not exists")

    def validate_type(self, value):
        if not Category.objects.filter(category=value).exists():
            raise serializers.ValidationError("category type does not exits")
        return value

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.main_image = validated_data['main_image']
        instance.description = validated_data['description']
        instance.available_rooms = validated_data['available_rooms']
        instance.country = validated_data['location']
        instance.number_of_bathrooms = validated_data['number_of_bathrooms']
        instance.discount = validated_data['discount']
        instance.amenities = validated_data['amenities']
        instance.rules = validated_data['rules']
        instance.is_active = validated_data['is_active']
        instance.is_verified = validated_data['is_verified']
        instance.check_in = validated_data['check_in']
        instance.check_out = validated_data['check_out']
        instance.save()

        return instance

    def create(self, validated_data):

        _owner = UserProfile.objects.get(uuid=validated_data['owner'])

        _category = Category.objects.get(category=validated_data['type'])
        validated_data['type'] = _category
        validated_data['owner'] = _owner.user
        apartment = Apartment.objects.create(
            **validated_data
        )

        return apartment


class ReviewSerializer(serializers.Serializer):
    given_by = serializers.CharField()
    apartment = serializers.CharField()
    review = serializers.CharField()
    uuid = serializers.CharField(read_only=True)

    def validate_given_by(self, value):
        giver_exists = UserProfile.objects.filter(uuid=value)
        if giver_exists.exists():
            return value
        raise serializers.ValidationError("user does not exists")

    def validate_apartment(self, value):
        giver_exists = Apartment.objects.filter(uuid=value)
        if giver_exists.exists():
            return value
        raise serializers.ValidationError("apartment does not exists")

    def create(self, validated_data):
        giver = UserProfile.objects.get(uuid=validated_data.pop("given_by"))
        apartment = Apartment.objects.get(uuid=validated_data.pop("apartment"))

        validated_data['given_by'] = giver.user
        validated_data['apartment'] = apartment

        review = Review.objects.create(**validated_data)
        return review
