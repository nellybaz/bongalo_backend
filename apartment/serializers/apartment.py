from apartment.models import Apartment, Category, Images
from rest_framework import serializers
from authentication.models import UserProfile
from authentication.serializers import UserProfileSerializerWithDetails


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
    max_guest_number = serializers.IntegerField()
    country = serializers.CharField()
    city = serializers.CharField()
    number_of_bathrooms = serializers.IntegerField()
    price = serializers.IntegerField()
    discount = serializers.FloatField()
    type = serializers.SlugRelatedField(
        slug_field="category",
        queryset=Category.objects.all())
    amenities = serializers.CharField()
    extras = serializers.CharField()
    rules = serializers.CharField(allow_blank=True)
    is_active = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    unavailable_from = serializers.DateField()
    unavailable_to = serializers.DateField()
    check_in = serializers.CharField()
    check_out = serializers.CharField()
    min_nights = serializers.IntegerField()
    max_nights = serializers.IntegerField()
    space = serializers.CharField()
    address = serializers.CharField()
    images = serializers.ListField(write_only=True)

    def validate_owner(self, value):
        _owner_ = UserProfile.objects.filter(uuid=value)
        if _owner_.exists():
            return value
        raise serializers.ValidationError("user does not exists")

    def update(self, instance, validated_data):
        print("called inside serializers")
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.price = validated_data['price']
        instance.available_rooms = validated_data['available_rooms']
        instance.max_guest_number = validated_data['max_guest_number']
        instance.country = validated_data['country']
        instance.city = validated_data['city']
        instance.number_of_bathrooms = validated_data['number_of_bathrooms']
        instance.type = validated_data['type']
        instance.amenities = validated_data['amenities']
        instance.extras = validated_data['extras']
        instance.rules = validated_data['rules']
        instance.check_in = validated_data['check_in']
        instance.check_out = validated_data['check_out']
        instance.min_nights = validated_data['min_nights']
        instance.max_nights = validated_data['max_nights']
        instance.space = validated_data['space']
        instance.address = validated_data['address']
        instance.save()
        return instance

    def create(self, validated_data):

        _owner = UserProfile.objects.get(uuid=validated_data['owner'])

        images = validated_data.pop("images")
        validated_data['owner'] = _owner
        apartment = Apartment.objects.create(
            **validated_data
        )
        for image in images:
            data = {
                'image': image,
                'apartment': apartment
            }
            Images.objects.create(
                **data
            )

        return apartment


class ApartmentWithOwnerSerializer(serializers.Serializer):
    owner = UserProfileSerializerWithDetails()

    class Meta:
        model = Apartment
        fields = ['title', 'main_image', 'price', 'owner']
