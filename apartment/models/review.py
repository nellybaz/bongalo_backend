from django.db import models
from uuid import uuid4
from .apartment import Apartment
from django.contrib.auth.models import User


class Review(models.Model):
    """
    Reviews are given to a particular apartment
    """
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    review = models.TextField(blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
