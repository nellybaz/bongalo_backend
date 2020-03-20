from django.db import models
from uuid import uuid4
from authentication.models import UserProfile
from apartment.models import Apartment


# Create your models here.
class Payment(models.Model):
    uuid = models.CharField(max_length=225, unique=True, blank=False, default=uuid4, primary_key=True)
    amount = models.FloatField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
