from django.contrib import admin
from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "resident_country", "origin_country", "phone", "national_id",
                    "is_active", "is_host", "is_admin", "created_at", "modified_at")
    fields = ("user", "address", "resident_country", "origin_country", "phone", "national_id", "is_active", "is_host",
              "is_admin")


admin.site.register(UserProfile, ProfileAdmin)
