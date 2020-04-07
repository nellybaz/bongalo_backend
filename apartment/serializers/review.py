from apartment.models import Apartment, Review
from rest_framework import serializers
from authentication.models import UserProfile


class ReviewSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    given_by = serializers.SlugRelatedField(queryset=UserProfile.objects.filter(is_active=True), slug_field="uuid")
    apartment = serializers.SlugRelatedField(queryset=Apartment.objects.filter(is_active=True), slug_field="uuid")
    review = serializers.CharField()
    uuid = serializers.CharField(read_only=True)

    # def validate_given_by(self, value):
    #     giver_exists = UserProfile.objects.filter(uuid=value)
    #     if giver_exists.exists():
    #         return value
    #     raise serializers.ValidationError("user does not exists")
    #
    # def validate_apartment(self, value):
    #     giver_exists = Apartment.objects.filter(uuid=value)
    #     if giver_exists.exists():
    #         return value
    #     raise serializers.ValidationError("apartment does not exists")

    def create(self, validated_data):
        # giver = UserProfile.objects.get(uuid=validated_data.pop("given_by"))
        # apartment = Apartment.objects.get(uuid=validated_data.pop("apartment"))
        #
        # validated_data['given_by'] = giver.user
        # validated_data['apartment'] = apartment

        review = Review.objects.create(**validated_data)
        return review
