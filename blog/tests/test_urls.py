from django.urls import reverse
from rest_framework.test import APITestCase


class BlogUrlsTest(APITestCase):
    def test_urls(self):
        self.assertEquals("/api/v1/blog/posts/all", reverse("get_all_blog_post"))
