from apartment.models import Apartment, Rating
from rest_framework import serializers
from authentication.models import UserProfile


class RatingSerializer(serializers.Serializer):
    apartment = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Apartment.objects.filter(
            is_active=True))
    given_by = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=UserProfile.objects.filter(
            is_active=True))
    rating = serializers.IntegerField()

    def create(self, validated_data):

        validated_data['given_by'] = validated_data['given_by'].user
        rating = Rating.objects.create(
            **validated_data
        )

        return rating
