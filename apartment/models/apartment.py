from django.db import models
from uuid import uuid4
from authentication.models import UserProfile


class Category(models.Model):
    """
    Category has to be any of the three
        1. Apartment
        2. Room
        3. Commercial
    """
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    category = models.CharField(
        max_length=100,
        default="Apartment",
        blank=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category


class Amenity(models.Model):
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    amenity = models.CharField(max_length=225, )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amenity


class Rule(models.Model):
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    rule = models.CharField(max_length=225, )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule


class Apartment(models.Model):
    """
    Commercial apartments are verified by owners
    """

    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, blank=False)
    # Stores image url which is store on a cloud
    main_image = models.CharField(max_length=225, blank=False)
    total_rooms = models.IntegerField(default=1, blank=False)
    available_rooms = models.IntegerField(default=1, blank=False)
    max_guest_number = models.IntegerField()
    description = models.TextField(blank=False)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    space = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=225, blank=False)
    city = models.CharField(max_length=225, blank=False)
    province = models.CharField(max_length=225, blank=False)
    country = models.CharField(max_length=225, blank=False, db_index=True)
    number_of_bathrooms = models.IntegerField(blank=False, default=1)
    price = models.IntegerField(default=0, blank=False, db_index=True)
    discount = models.FloatField(max_length=225, blank=False)
    amenities = models.TextField(default="")  # String separated by ,
    extras = models.TextField(default="")  # String separated by ,
    rules = models.TextField(blank=True, default="")  # String separated by ,
    is_active = models.BooleanField(default=True, blank=False)
    is_verified = models.BooleanField(
        default=False, blank=False)  # Used for commercial properties
    unavailable_from = models.DateField(blank=False)
    unavailable_to = models.DateField(blank=False)
    min_nights = models.IntegerField()
    max_nights = models.IntegerField()
    check_in = models.CharField(max_length=10,
                                blank=True)  # Timezone is Africa/Kigali
    check_out = models.CharField(max_length=10,
                                 blank=True)  # Timezone is Africa/Kigali
    is_available = models.BooleanField(default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
