from django.db import models
from django.contrib.auth.models import User


# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=225, blank=True, )
    resident_country = models.CharField(max_length=225, blank=True, )
    origin_country = models.CharField(max_length=225, blank=True, )
    phone = models.CharField(max_length=225, blank=True, )
    national_id = models.FileField(blank=True, )
    passport = models.FileField(blank=True, )
    is_active = models.BooleanField(blank=True, default=True)
    is_host = models.BooleanField(blank=True, default=False)
    is_admin = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


