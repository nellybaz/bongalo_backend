from django.contrib import admin
from apartment.models import (Apartment, Category, Review,
                              Images, Amenity, Booking)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'image')
    # fields = ('apartment', 'image')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'category')
    fields = ('uuid', 'category')


class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "description",
        "main_image",
        "available_rooms",
        "number_of_bathrooms",
        "max_guest_number",
        "city",
        "space",
        "address",
        "country",
        "price",
        "discount",
        "type",
        "amenities",
        "rules",
        "is_verified",
        "is_active",
        "unavailable_from",
        "unavailable_to",
        "check_in",
        "check_out")


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "given_by",
        "apartment",
        "review",
        "is_active",
        "created_at")


class AmenityAdmin(admin.ModelAdmin):
    list_display = ("amenity", "created_at")


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "apartment",
        "client",
        "number_of_rooms",
        "number_of_guest",
        "date_from",
        "date_to",
        # "check_in",
        # "check_out"
    )


admin.site.register(Amenity, AmenityAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
