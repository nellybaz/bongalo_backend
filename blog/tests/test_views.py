from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class BlogPostViewTest(APITestCase):
    def setUp(self):
        self.all_apartments = reverse("get_all_blog_post")

    def test_get_blog_posts(self):
        response = self.client.get(self.all_apartments)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['responseCode'], 1)
        # self.assertEquals()
