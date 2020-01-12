from apartment.models import Apartment
from rest_framework import serializers


class ApartmentSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)

    class Meta:
        model = Apartment
        fields = ["uid", "title", "owner", "description", "available_rooms", "location", "price", "discount", "type",
                  "amenities", "rules", "check_in", "check_out"]

