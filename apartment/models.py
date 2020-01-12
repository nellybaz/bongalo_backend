from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Apartment(models.Model):
    uid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, blank=False)
    main_image = models.ImageField(blank=False)
    available_rooms = models.IntegerField(default=1, blank=False)
    description = models.TextField(blank=False)
    type = models.CharField(max_length=200, blank=False)
    location = models.CharField(max_length=225, blank=False)
    price = models.CharField(max_length=225, blank=False)
    discount = models.CharField(max_length=225, blank=False)
    amenities = models.CharField(max_length=225, blank=False)  # String separated by +
    rules = models.CharField(max_length=225, blank=False)  # String separated by +
    check_in = models.DateTimeField(blank=False)  # Timezone is Africa/Kigali
    check_out = models.DateTimeField(blank=False)  # Timezone is Africa/Kigali
    created_at = models.DateTimeField(auto_now_add=True)
    # name = models.CharField(max_length=225, blank=False)
    # name = models.CharField(max_length=225, blank=False)
    # name = models.CharField(max_length=225, blank=False)
    # name = models.CharField(max_length=225, blank=False)
    # name = models.CharField(max_length=225, blank=False)
    # name = models.CharField(max_length=225, blank=False)
    # name = models.CharField(max_length=225, blank=False)


class Images(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.CharField(max_length=225, blank=False)
