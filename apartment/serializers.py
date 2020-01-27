from apartment.models import Apartment, Review
from rest_framework import serializers
from authentication.models import UserProfile
from .models import Category


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
    location = serializers.CharField()
    number_of_bathrooms = serializers.IntegerField()
    price = serializers.IntegerField()
    discount = serializers.FloatField()
    type = CategorySerializer()
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

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):

        _owner = UserProfile.objects.get(uuid=validated_data['owner'])

        _category = Category.objects.get(category=validated_data['type']['category'])
        validated_data['type'] = _category
        validated_data['owner'] = _owner.user
        apartment = Apartment.objects.create(
            **validated_data
        )

        return apartment


class ReviewSerializer(serializers.ModelSerializer):
    model = Review
    field = ["apartment", "review"]
