from django.db import models
from uuid import uuid4


class Tag(models.Model):
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    title = models.CharField(
        max_length=100,
        default='')
    body = models.TextField()
    image = models.CharField(max_length=225)
    is_featured = models.BooleanField(default=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

