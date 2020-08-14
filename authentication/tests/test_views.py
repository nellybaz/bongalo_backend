from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User, UserProfile
from rest_framework.test import APIClient
from unittest import skip


@skip("Not working for now")
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()
        self.user = User.objects.create_user(
            username="bass106@gmail.comz14xx",
            email="bass106@gmail.comz14xx",
            password="pass"
        )
        # self.user = User.objects.get(username="bass106@gmail.comz14xx")

    def test_register_user_view_success(self):

        response = self.client.post(reverse("register_user"),
                                    {"username": "new_user1x",
                                     "email": "newuser1x@gmail.com",
                                     "password": "password",
                                     "first_name": "first_name",
                                     "last_name": "last_name",
                                     "is_admin": False,
                                     "is_active": False})
        user = User.objects.get(username="new_user1x")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(user.email, "newuser1x@gmail.com")

    def test_user_profile_created_at_register(self):
        response = self.client.post(reverse("register_user"),
                                    {"username": "new_user1x",
                                     "email": "newuser1x@gmail.com",
                                     "password": "password",
                                     "first_name": "first_name",
                                     "last_name": "last_name",
                                     "is_admin": False,
                                     "is_active": False})
        user = User.objects.get(username="new_user1x")
        profile = UserProfile.objects.get(user=user)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(profile.first_name, "first_name")

    def test_register_user_view_no_username(self):

        response = self.client.post(reverse("register_user"),
                                    {"email": "newuser1@gmail.com",
                                     "password": "password",
                                     "first_name": "first_name",
                                     "last_name": "last_name",
                                     "is_admin": False,
                                     "is_active": False})
        self.assertEquals(response.status_code, 400)

    def test_login_view_success(self):
        # token = Token.objects.create(user=user)
        # print(token.key)
        # api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.api_client.force_authenticate(user=self.user)
        print(self.user.email, self.user.password)
        request = self.api_client.get(
            reverse(
                "login_user", args=[
                    self.user.username]))

        self.assertEquals(
            request.status_code,
            200,
            "True if login success else False")
