from apartment.models import Apartment, Category, Images
from rest_framework import serializers
from authentication.models import UserProfile


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
    rules = serializers.CharField(allow_blank=True)
    is_active = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    unavailable_from = serializers.DateField()
    unavailable_to = serializers.DateField()
    check_in = serializers.CharField()
    check_out = serializers.CharField()
    min_nights = serializers.IntegerField()
    max_nights = serializers.IntegerField()
    images = serializers.ListField(write_only=True)

    def validate_owner(self, value):
        _owner_ = UserProfile.objects.filter(uuid=value)
        if _owner_.exists():
            return value
        raise serializers.ValidationError("user does not exists")

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.price = validated_data['price']
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
