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
    uuid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4, primary_key=True)
    category = models.CharField(max_length=100, default="Apartment", blank=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category


class Amenity(models.Model):
    uuid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4, primary_key=True)
    amenity = models.CharField(max_length=225, )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amenity


class Rule(models.Model):
    uuid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4, primary_key=True)
    rule = models.CharField(max_length=225, )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule


class Apartment(models.Model):
    """
    Commercial apartments are verified by owners
    """

    uuid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, blank=False)
    main_image = models.CharField(max_length=225, blank=False)  # Stores image url which is store on a cloud
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
    is_verified = models.BooleanField(default=False, blank=False)  # Used for commercial properties
    unavailable_from = models.DateField(blank=False)
    unavailable_to = models.DateField(blank=False)
    min_nights = models.IntegerField()
    max_nights = models.IntegerField()
    check_in = models.TimeField(blank=True)  # Timezone is Africa/Kigali
    check_out = models.TimeField(blank=True)  # Timezone is Africa/Kigali
    is_available = models.BooleanField(default=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ActiveBooking(models.Model):
    uuid = models.CharField(default=uuid4, max_length=225, blank=False, primary_key=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=False)
    date_from = models.DateField(blank=False)
    date_to = models.DateField(blank=False)
    check_in = models.TimeField(blank=False)
    check_out = models.TimeField(blank=False)
    number_of_rooms = models.IntegerField(default=1, blank=False)
    number_of_guest = models.IntegerField(default=1, blank=False)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class BookingArchive(models.Model):
    uuid = models.CharField(default=uuid4, max_length=225, blank=False, primary_key=True)
    booking = models.ForeignKey(ActiveBooking, on_delete=models.CASCADE)
    was_completed = models.BooleanField(default=True)
    was_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    """
    Reviews are given to a particular apartment
    """
    uuid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4, primary_key=True)
    given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    review = models.TextField(blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Images(models.Model):
    uuid = models.CharField(default=uuid4, unique=True, max_length=225, primary_key=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.ImageField(max_length=225, blank=False)
    image1 = models.ImageField(max_length=225, blank=False)
    image2 = models.ImageField(max_length=225, blank=False)
    image3 = models.ImageField(max_length=225, blank=False)
    image4 = models.ImageField(max_length=225, blank=False)
    image5 = models.ImageField(max_length=225, blank=False)
    image6 = models.ImageField(max_length=225, blank=False)
    image7 = models.ImageField(max_length=225, blank=False)
    image8 = models.ImageField(max_length=225, blank=False)
    image9 = models.ImageField(max_length=225, blank=False)
    image10 = models.ImageField(max_length=225, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    uuid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4, primary_key=True)
    given_by = models.OneToOneField(User, on_delete=models.CASCADE)
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

