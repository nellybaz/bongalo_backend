from apartment.models import Apartment, Review, Category, Images, ActiveBooking, Rating
from rest_framework import serializers
from authentication.models import UserProfile


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Category
        fields = ["category"]


# class ImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Images
#         fields = ('apartment', 'image')


class ApartmentSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    title = serializers.CharField()
    owner = serializers.CharField()
    main_image = serializers.CharField()
    description = serializers.CharField()
    available_rooms = serializers.IntegerField()
    max_guest_number = serializers.IntegerField()
    country = serializers.CharField()
    number_of_bathrooms = serializers.IntegerField()
    price = serializers.IntegerField()
    discount = serializers.FloatField()
    type = serializers.SlugRelatedField(slug_field="category", queryset=Category.objects.all())
    amenities = serializers.CharField()
    rules = serializers.CharField()
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

    # def validate_type(self, value):
    #     if not Category.objects.filter(category=value).exists():
    #         raise serializers.ValidationError("category type does not exits")
    #     return value

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        # instance.main_image = validated_data['main_image']
        instance.description = validated_data['description']
        instance.price = validated_data['price']
        # instance.available_rooms = validated_data['available_rooms']
        # instance.country = validated_data['country']
        # instance.number_of_bathrooms = validated_data['number_of_bathrooms']
        # instance.max_guest_number = validated_data['max_guest_number']
        # instance.discount = validated_data['discount']
        # instance.amenities = validated_data['amenities']
        # instance.rules = validated_data['rules']
        # instance.is_active = validated_data['is_active']
        # instance.is_verified = validated_data['is_verified']
        # instance.check_in = validated_data['check_in']
        # instance.check_out = validated_data['check_out']
        # instance.available_from = validated_data["available_from"] if "available_from" in validated_data else instance.available_from
        # instance.available_to = validated_data["available_to"] if "available_to" in validated_data else instance.available_to
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


class ImageSerializer(serializers.Serializer):
    apartment = serializers.SlugRelatedField(slug_field="uuid", queryset=Apartment.objects.all())
    image = serializers.CharField()

    def create(self, validated_data):
        image = Images.objects.create(
            **validated_data
        )

        return image


class BookingSerializer(serializers.Serializer):
    client = serializers.CharField()
    apartment = serializers.SlugRelatedField(slug_field="uuid", queryset=Apartment.objects.filter(is_active=True))
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    check_in = serializers.TimeField()
    check_out = serializers.TimeField()
    number_of_rooms = serializers.IntegerField()
    number_of_guest = serializers.IntegerField()

    def validate_client(self, value):
        if not UserProfile.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("user does not exists")
        return value

    def validate(self, attrs):
        # Check for zero number of room booking
        if attrs['number_of_rooms'] == 0:
            raise serializers.ValidationError("you cannot book 0 rooms")
        # Check active bookings for the apartment to know if room is available
        active_bookings = ActiveBooking.objects.filter(apartment=attrs['apartment'], is_active=True)
        booked_room_for_apartment = 0
        for booking in active_bookings:
            booked_room_for_apartment += booking.number_of_rooms

        available_rooms = attrs['apartment'].available_rooms - booked_room_for_apartment
        if attrs['number_of_rooms'] > available_rooms:
            raise serializers.ValidationError("not enough rooms, available rooms are " + str(available_rooms))

        if attrs['date_from'] < attrs['apartment'].available_from:
            raise serializers.ValidationError("apartment is not available at this time")

        if attrs['date_to'] > attrs['apartment'].available_to:
            raise serializers.ValidationError("apartment is not available till this time")

        return attrs

    def create(self, validated_data):

        user = UserProfile.objects.get(uuid=validated_data['client']).user

        validated_data['client'] = user
        booking = ActiveBooking.objects.create(
            **validated_data
        )

        return booking


class RatingSerializer(serializers.Serializer):
    apartment = serializers.SlugRelatedField(slug_field="uuid", queryset=Apartment.objects.filter(is_active=True))
    given_by = serializers.SlugRelatedField(slug_field="uuid", queryset=UserProfile.objects.filter(is_active=True))
    rating = serializers.IntegerField()

    def create(self, validated_data):

        validated_data['given_by'] = validated_data['given_by'].user
        rating = Rating.objects.create(
            **validated_data
        )

        return rating
