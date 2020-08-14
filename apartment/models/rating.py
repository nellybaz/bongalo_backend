from django.db import models
from uuid import uuid4
from .apartment import Apartment
from django.contrib.auth.models import User


class Rating(models.Model):
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    given_by = models.OneToOneField(User, on_delete=models.CASCADE)
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    rating = models.IntegerField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
