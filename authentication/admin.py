from django.contrib import admin
from .models import UserProfile, PaymentMethod, PinVerify, PasswordReset, UserSubscribe


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "address",
        "resident_country",
        "origin_country",
        "phone",
        "profile_image",
        "national_id",
        "is_active",
        "is_admin",
        "created_at",
        "modified_at",
        "national_id",
        "passport",
        "is_verified")


admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(PaymentMethod)
admin.site.register(PinVerify)
admin.site.register(PasswordReset)
admin.site.register(UserSubscribe)
