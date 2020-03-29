from blog.models import Post
from rest_framework import serializers


class BlogPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['uuid', 'title', 'body', 'tag', 'created_at', 'is_featured']
