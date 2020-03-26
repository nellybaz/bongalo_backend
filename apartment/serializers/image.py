from apartment.models import Images, Apartment
from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    apartment = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Apartment.objects.all())
    image = serializers.CharField()

    def create(self, validated_data):
        image = Images.objects.create(
            **validated_data
        )

        return image
