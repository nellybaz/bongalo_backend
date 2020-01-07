from django.db import models
import uuid


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.CharField(max_length=100, blank=True, default='')
    # image1 = models.Image
