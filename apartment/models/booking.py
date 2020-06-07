from django.db import models
from uuid import uuid4
from authentication.models import UserProfile
from .apartment import Apartment
from datetime import  timedelta, datetime

class Booking(models.Model):
    uuid = models.CharField(
        default=uuid4,
        max_length=225,
        blank=False,
        primary_key=True)
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False)
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

    @property
    def booking_price(self):
        apartment_price = self.apartment.price
        time_difference = self.date_to - self.date_from
        numbers_of_days = time_difference.total_seconds() / 86400
        total_price = apartment_price * numbers_of_days
        return total_price

    @property
    def cancellation_fees(self):
        """
        return the cancellation fees
        """
        today_date = datetime.now().date()
        days_elapsed = abs(today_date - self.date_from).days
        if days_elapsed <= 2:
            return 0.5
        elif days_elapsed > 2:
            return 1
        elif today_date > self.date_from:
            return 0