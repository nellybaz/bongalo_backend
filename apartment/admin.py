from django.contrib import admin
from apartment.models import Apartment


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "description", "available_rooms", "location", "price", "discount",
                    "type", "amenities", "rules", "check_in", "check_out")
    fields = ("title", "owner", "description", "available_rooms", "location", "price", "discount", "type",
              "amenities", "rules", "check_in", "check_out")


admin.site.register(Apartment, ApartmentAdmin)
