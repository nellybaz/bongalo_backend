from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from datetime import datetime


class Category(models.Model):
    """
    Category has to be any of the three
        1. Apartment
        2. Room
        3. Commercial
    """
    uid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4)
    category = models.CharField(max_length=100, default="Apartment", blank=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category


class Apartment(models.Model):
    """
    Commercial apartments are verified by owners
    """

    uid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, blank=False)
    main_image = models.CharField(max_length=225, blank=False)  # Stores image url which is store on a cloud
    available_rooms = models.IntegerField(default=1, blank=False)
    description = models.TextField(blank=False)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=225, blank=False)
    number_of_bathrooms = models.IntegerField(max_length=10, blank=False, default=1)
    price = models.IntegerField(default=0, blank=False)
    discount = models.FloatField(max_length=225, blank=False)
    amenities = models.CharField(max_length=225, blank=False)  # String separated by ,
    rules = models.CharField(max_length=225, blank=False)  # String separated by ,
    is_active = models.BooleanField(default=True, blank=False)
    is_verified = models.BooleanField(default=False, blank=False)  # Used for commercial properties
    check_in = models.DateTimeField(blank=False)  # Timezone is Africa/Kigali
    check_out = models.DateTimeField(blank=False)  # Timezone is Africa/Kigali
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Reviews are given to a particular apartment
    """
    uid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    review = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Images(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.CharField(max_length=225, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
