from django.db import models
from uuid import uuid4
# from gcloud import storage


class Event(models.Model):
    uuid = models.CharField(
        max_length=225,
        unique=True,
        blank=False,
        default=uuid4,
        primary_key=True)
    name = models.CharField(max_length=225)
    image = models.CharField(max_length=225)
    description = models.TextField()
    location = models.CharField(max_length=225)
    category = models.CharField(max_length=1)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     print("image here is here")
    #     print(self.image)
    #
    #     # Import
    #
    #
    #     # Initialize
    #     client = storage.Client()
    #     bucket = client.get_bucket('gs://bongalo-37967.appspot.com')
    #
    #     # Download
    #     # blob = bucket.get_blob('remote/path/to/file.txt')
    #     # print("download section")
    #     # blob.download_as_string()
    #
    #     # Upload
    #     blob2 = bucket.blob('events/{0}'.format(self.name))
    #     res = blob2.upload_from_file(self.image)
    #     print(res)
    #
    #     super().save()

