from blog.models import Post, Image, Tag
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class BlogPostSerializers(serializers.ModelSerializer):
    images = ImageSerializer(many=True,)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['uuid', 'title', 'body', 'tags', 'created_at', 'is_featured', 'images']
