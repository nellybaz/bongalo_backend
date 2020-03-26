from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.views import UserRegisterViews, LoginView
from unittest import skip


@skip('not working now')
class TestUrls(SimpleTestCase):

    def test_register_user_url(self):
        url = reverse("register_user")
        self.assertEquals(resolve(url).func.view_class, UserRegisterViews)

    def test_login_user_url(self):
        url = reverse("login_user", args=["example_user"])
        self.assertEquals(resolve(url).func.view_class, LoginView)

    @skip('We dont know if the product exist yet')
    def test_update_user_url(self):
        url = reverse("update_user", args=["example_user"])
        self.assertEquals(resolve(url).func.view_class, UpdateAPIView)
