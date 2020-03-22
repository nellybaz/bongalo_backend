from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from authentication.tests.factories import UserProfileFactory
from .utils import apartment_field_names
from .factories import ApartmentWithImagesFactory, CategoryFactory
from ..models import Apartment


class ApartmentViewSetTestCase(APITestCase):
    """
    Test apartments views
    """

    def setUp(self):
        self.user_profile = UserProfileFactory()
        self.user_profile.save()
        self.client.force_authenticate(self.user_profile.user)
        self.category = CategoryFactory()
        self.add_apartment = reverse('add_apartment')
        self.update_apartment = reverse('update_apartment')
        self.delete_apartment = reverse('delete_apartment')
        self.search_apartments = reverse('search_apartments')
        self.all_apartments = reverse('all_apartments')
        self.new_apartment_data = {
            "title": 'a-fakename',
            "owner": 'should-come from app',
            "main_image": 'an url from cloudinary',
            "description": 'this is my house',
            "available_rooms": 5,
            "max_guest_number": 7,
            "country": "DRC Congo",
            "number_of_bathrooms": 5,
            "price": 1000,
            "discount": 0.5,
            "type": 'Commercial',
            "amenities": "None",
            "rules": "Don't smoke in my house",
            "unavailable_from": '2020-03-15',
            "unavailable_to": '2020-03-20',
            "check_in": "should be a date I don't know why",
            "check_out": "should be a date I don't know why",
            "min_nights": 5,
            "max_nights": 7,
            "images": ['this is a test image one', 'this is a test image two']}

    def test_list_apartments(self):
        apartments = [ApartmentWithImagesFactory.create() for i in range(6)]
        response = self.client.get(self.all_apartments)
        self.assertEqual(len(apartments), len(response.data.get('results')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        apartment_field_names.remove('owner')
        for field in apartment_field_names:
            self.assertEqual(
                set(str(apartment.get(field)) for apartment in response.data.get('results')),
                set(str(getattr(apartment, field)) for apartment in apartments)
            )

    def test_can_create_apartment(self):
        old_count = Apartment.objects.count()
        self.new_apartment_data['owner'] = self.user_profile.uuid
        self.new_apartment_data['type'] = self.category.category
        response = self.client.post(
            self.add_apartment,
            data=self.new_apartment_data)
        self.assertEqual(response.data.get('statusCode'), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Apartment.objects.count(), old_count + 1)
        apartment = Apartment.objects.all().first()
        for field_name in self.new_apartment_data.keys():
            # TODO : check behavior with images and owner
            if field_name not in ['owner', 'images']:
                self.assertEqual(
                    str(getattr(
                        apartment,
                        field_name)),
                    str(self.new_apartment_data.get(field_name)))

    def test_raise_error_when_creating_data(self):
        pass
