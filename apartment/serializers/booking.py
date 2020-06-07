from apartment.models import Apartment, Booking
from rest_framework import serializers
from authentication.models import UserProfile
from authentication.serializers import UserProfileSerializer, UserProfileSerializerWithDetails
from apartment.serializers.apartment import ApartmentWithOwnerSerializer


class BookingSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    client = serializers.CharField()
    apartment = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Apartment.objects.filter(
            is_active=True))
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    # check_in = serializers.TimeField()
    # check_out = serializers.TimeField()
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
        active_bookings = Booking.objects.filter(
            apartment=attrs['apartment'], is_active=True, is_completed=True)
        booked_room_for_apartment = len(active_bookings)

        available_rooms = attrs['apartment'].available_rooms - \
            booked_room_for_apartment
        if attrs['number_of_rooms'] > available_rooms:
            raise serializers.ValidationError(
                "not enough rooms, available rooms are " +
                str(available_rooms))

        if attrs['apartment'].unavailable_from <= attrs['date_from'] <= attrs['apartment'].unavailable_to:
            raise serializers.ValidationError(
                "apartment is not available at this time")
        #
        # if attrs['date_to'] > attrs['apartment'].available_to:
        #     raise serializers.ValidationError(
        #         "apartment is not available till this time")

        return attrs

    def create(self, validated_data):

        user = UserProfile.objects.get(uuid=validated_data['client'])

        validated_data['client'] = user
        booking = Booking.objects.create(
            **validated_data
        )

        return booking


class BookingWithApartmentSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    client = UserProfileSerializerWithDetails()
    apartment = ApartmentWithOwnerSerializer()
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    number_of_rooms = serializers.IntegerField()
    number_of_guest = serializers.IntegerField()
