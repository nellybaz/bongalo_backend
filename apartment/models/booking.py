from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from .apartment import Apartment


class Booking(models.Model):
    uuid = models.CharField(
        default=uuid4,
        max_length=225,
        blank=False,
        primary_key=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        blank=False)
    date_from = models.DateField(blank=False)
    date_to = models.DateField(blank=False)
    # check_in = models.TimeField(blank=False)
    # check_out = models.TimeField(blank=False)
    number_of_rooms = models.IntegerField(default=1, blank=False)
    number_of_guest = models.IntegerField(default=1, blank=False)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# class BookingArchive(models.Model):
#     uuid = models.CharField(
#         default=uuid4,
#         max_length=225,
#         blank=False,
#         primary_key=True)
#     booking = models.ForeignKey(ActiveBooking, on_delete=models.CASCADE)
#     was_completed = models.BooleanField(default=True)
#     was_canceled = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
