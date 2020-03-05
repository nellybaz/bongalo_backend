from django.contrib import admin
from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "resident_country", "origin_country", "phone", "national_id",
                    "is_active", "is_admin", "created_at", "modified_at", "national_id", "passport",
                    "is_verified")


admin.site.register(UserProfile, ProfileAdmin)
