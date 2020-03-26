from django.db import models
from uuid import uuid4
from .apartment import Apartment


class Images(models.Model):
    uuid = models.CharField(
        default=uuid4,
        unique=True,
        max_length=225,
        primary_key=True)
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="images")
    image = models.CharField(max_length=225, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
