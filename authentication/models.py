from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


# User profile model
class UserProfile(models.Model):
    uuid = models.CharField(primary_key=True, unique=True, default=uuid4, max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=225, blank=True, )
    resident_country = models.CharField(max_length=225, blank=True, )
    origin_country = models.CharField(max_length=225, blank=True, )
    phone = models.CharField(max_length=225, blank=True, )
    national_id = models.CharField(blank=True, max_length=225)
    is_verified = models.BooleanField(default=False, blank=True)
    passport = models.CharField(blank=True, max_length=225)
    is_active = models.BooleanField(blank=False, default=False)
    is_admin = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)



