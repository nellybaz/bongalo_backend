from django.contrib import admin
from apartment.models import Apartment, Category, Review, Images


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'image')
    fields = ('apartment', 'image')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'category')
    fields = ('uuid', 'category')


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "description", "main_image", "available_rooms", "number_of_bathrooms", "address", "price", "discount",
                    "type", "amenities", "rules", "is_verified", "is_active", "check_in", "check_out")
    # fields = ("title", "owner", "description", "main_image", "available_rooms", "number_of_bathrooms", "location", "price", "discount", "type",
    #           "amenities", "is_verified", "is_active", "rules", "check_in", "check_out")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("given_by", "apartment", "review", "is_active", "created_at")


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
