from django.contrib import admin
from .models import Post, Tag, Image


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Image)