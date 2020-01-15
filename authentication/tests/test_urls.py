from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.views import RegisterAPIView, LoginAPIView, UpdateAPIView


class TestUrls(SimpleTestCase):

    def test_register_user_url(self):
        url = reverse("register_user")
        self.assertEquals(resolve(url).func.view_class, RegisterAPIView)

    def test_login_user_url(self):
        url = reverse("login_user", args=["example_user"])
        self.assertEquals(resolve(url).func.view_class, LoginAPIView)

    def test_update_user_url(self):
        url = reverse("update_user", args=["example_user"])
        self.assertEquals(resolve(url).func.view_class, UpdateAPIView)
