from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


# User profile model
class UserProfile(models.Model):
    uuid = models.CharField(
        primary_key=True,
        unique=True,
        default=uuid4,
        max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=225, blank=True, )
    description = models.TextField(default="")
    resident_city = models.CharField(max_length=225, blank=True, )
    resident_country = models.CharField(max_length=225, blank=True, )
    origin_country = models.CharField(max_length=225, blank=True, )
    phone = models.CharField(max_length=225, blank=True, )
    profile_image = models.CharField(max_length=225, default="", blank=True)
    national_id = models.CharField(blank=True, max_length=225)
    is_verified = models.BooleanField(default=False, blank=True)
    passport = models.CharField(blank=True, max_length=225)
    is_active = models.BooleanField(blank=False, default=False)
    is_admin = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    verification_status = models.CharField(max_length=1, default="U")

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class PaymentMethod(models.Model):
    uuid = models.CharField(
        primary_key=True,
        unique=True,
        default=uuid4,
        max_length=100)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    momo_number = models.CharField(max_length=20, default="")
    momo_name = models.CharField(max_length=20, default="")
    bank_name = models.CharField(max_length=50, default="")
    account_name = models.CharField(max_length=50, default="")
    account_number = models.CharField(max_length=50, default="")
    swift_code = models.CharField(max_length=20, default="")
    created_at = models.DateTimeField(auto_now_add=True)


class PinVerify(models.Model):
    uuid = models.CharField(
        primary_key=True,
        unique=True,
        default=uuid4,
        max_length=100)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    pin = models.CharField(max_length=10)


class PasswordReset(models.Model):
    uuid = models.CharField(
        primary_key=True,
        unique=True,
        default=uuid4,
        max_length=100)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reset_key = models.CharField(max_length=225)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class UserSubscribe(models.Model):
    uuid = models.CharField(
        primary_key=True,
        unique=True,
        default=uuid4,
        max_length=100)
    email = models.EmailField(max_length=225, default="")
