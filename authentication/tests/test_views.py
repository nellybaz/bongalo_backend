from django.test import TestCase, Client
from django.urls import reverse, resolve
from authentication.models import User, UserProfile
from rest_framework.test import APIRequestFactory, force_authenticate
from authentication.views import LoginAPIView
from rest_framework.authtoken.models import Token


class TestViews(TestCase):
    def setup(self):
        self.client = Client()

    def test_register_user_view_success(self):

        response = self.client.post(reverse("register_user"), {"username": "new_user1x", "email": "newuser1x@gmail.com",
                                                               "password": "password", "first_name": "first_name",
                                                               "last_name": "last_name"})
        user = User.objects.get(username="new_user1x")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(user.email, "newuser1x@gmail.com")

    def test_user_profile_created_at_register(self):
        response = self.client.post(reverse("register_user"), {"username": "new_user1x", "email": "newuser1x@gmail.com",
                                                               "password": "password", "first_name": "first_name",
                                                               "last_name": "last_name"})
        user = User.objects.get(username="new_user1x")
        profile = UserProfile.objects.get(user=user)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(profile.first_name, "first_name")

    def test_register_user_view_no_username(self):

        response = self.client.post(reverse("register_user"), {"email": "newuser1@gmail.com", "password": "password",
                                                               "first_name": "first_name", "last_name": "last_name"})
        self.assertEquals(response.status_code, 400)

    # def test_login_view_success(self):
    #     factory = APIRequestFactory()
    #     user = User.objects.create(
    #         username="test_user1x",
    #         email="test_user1x@email.com",
    #         password="pass"
    #     )
    #     Token.objects.create(
    #
    #     )
    #     # user = User.objects.get(username="")
    #     view = LoginAPIView.as_view()
    #     request = factory.get('login/test_user1x@email.com')
    #     force_authenticate(request, user=user)
    #     response = view(request)
    #     self.assertEquals(response.status_code, 200)

    # def test_login_view_no_username(self):
    #
    #     response = self.client.post(reverse("login_user"), {"email": "newuser1@gmail.com", "password": "password", "first_name": "first_name", "last_name": "last_name"})
    #     self.assertEquals(response.status_code, 400)  # Created failed, no username
