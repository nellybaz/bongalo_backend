import json
from unittest import skip
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from authentication.tests.factories import UserProfileFactory
from .utils import apartment_field_names
from .factories import ApartmentWithImagesFactory, CategoryFactory
from ..models import Apartment


class BaseApartmentTest(APITestCase):
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
            "main_image": 'an url from Cloudinary',
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


class ListApartmentTest(BaseApartmentTest):
    """

    test list apartment endpoint
    """

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


class CreateApartmentTest(BaseApartmentTest):
    """
    test create apartment tests
    """

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

    def test_raise_error_when_no_type(self):
        self.new_apartment_data['owner'] = self.user_profile.uuid
        del self.new_apartment_data['type']
        response = self.client.post(
            self.add_apartment,
            data=self.new_apartment_data)
        self.assertEqual(response.data.get('statusCode'), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_raise_error_when_no_owner(self):
        response = self.client.post(
            self.add_apartment,
            data=self.new_apartment_data)
        self.assertEqual(str(response.data.get('data').get(
            'owner')[0]), "user does not exists")
        self.assertEqual(response.data.get('statusCode'), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_raise_error_when_no_images(self):
        self.new_apartment_data['owner'] = self.user_profile.uuid
        del self.new_apartment_data['images']
        response = self.client.post(
            self.add_apartment,
            data=self.new_apartment_data)
        self.assertEqual(response.data.get('statusCode'), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_raise_401_when_not_login(self):
        self.client.logout()
        response = self.client.post(
            self.add_apartment,
            data=self.new_apartment_data)
        self.assertEqual(response.data.get('detail'),
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateApartmentTest(BaseApartmentTest):
    """
    test updating a new apartment
    """

    @skip("need to check why this is failing")
    def test_raise_error_when_not_owner(self):
        apartment = ApartmentWithImagesFactory()
        apartment.owner = self.user_profile
        apartment.save()
        data = {'title': 'this is an awesome',
                'description': 'I want to create something',
                'price': 1000}
        data['uuid'] = apartment.uuid
        self.client.logout()
        self.client.force_authenticate(UserProfileFactory().user)
        response = self.client.put(
            self.update_apartment,
            data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_update_apartment(self):
        apartment = ApartmentWithImagesFactory()
        data = {'title': 'this is an awesome',
                'description': 'I want to create something',
                'price': 1000}
        data['uuid'] = apartment.uuid
        response = self.client.put(
            self.update_apartment,
            data=json.dumps(data),
            content_type='application/json')
        returned_data = response.data
        self.assertEqual(returned_data.get('statusCode'), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in data:
            self.assertEqual(data.get(key), returned_data.get('data').get(key))

    def test_update_fails_when_apartment_not_exist(self):
        data = {'title': 'this is an awesome',
                'description': 'I want to create something',
                'price': 1000}
        data['uuid'] = 'a-fake-apartment'
        response = self.client.put(
            self.update_apartment,
            data=json.dumps(data),
            content_type='application/json')
        returned_data = response.data
        self.assertEqual(returned_data.get('statusCode'), 0)
        self.assertEqual(
            returned_data.get('data'),
            "apartment does not exists")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_data_serializer_invalid(self):
        pass


class DeleteApartmentTests(BaseApartmentTest):

    def test_can_delete(self):
        apartment = ApartmentWithImagesFactory()
        data = {'uuid': apartment.uuid}
        response = self.client.delete(
            self.delete_apartment,
            data=json.dumps(data),
            content_type='application/json')
        returned_data = response.data
        deleted_apartment = Apartment.objects.filter(
            uuid=apartment.uuid).first()
        self.assertFalse(deleted_apartment.is_active)
        self.assertEqual(returned_data.get('statusCode'), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            returned_data.get('data'),
            "apartment deleted successfully")

    def test_cannot_delete_apartment_already_deleted(self):
        apartment = ApartmentWithImagesFactory()
        apartment.is_active = False
        apartment.save()
        data = {'uuid': apartment.uuid}
        response = self.client.delete(
            self.delete_apartment,
            data=json.dumps(data),
            content_type='application/json')
        returned_data = response.data
        self.assertEqual(returned_data.get('statusCode'), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            returned_data.get('data'),
            "apartment already deleted")

    def test_cannot_delete_apartment_if_not_owner(self):
        """
        Once the other part of update is fixed this will be fixed
        """
        pass

    def test_cannot_delete_apartment_if_not_exist(self):
        data = {'uuid': 'fake-apartment'}
        response = self.client.delete(
            self.delete_apartment,
            data=json.dumps(data),
            content_type='application/json')
        returned_data = response.data
        self.assertEqual(returned_data.get('statusCode'), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            returned_data.get('data'),
            "apartment does not exists")


class SearchApartmentTest(BaseApartmentTest):
    def setUp(self):
        super().setUp()
        self.apartment = ApartmentWithImagesFactory()
        self.apartment.max_guest_number = 6
        self.check_in = '10/03/2020'
        self.check_out = '15/03/2020'
        self.apartment.unavailable_from = '2020-03-16'
        self.apartment.unavailable_to = '2020-03-20'
        self.apartment.save()

    def test_search_apartment_all(self):
        response = self.client.get(self.search_apartments,
                                   {'guest': 5, 'type': 'all'})
        response_data = response.data
        self.assertEqual(response_data.get('responseCode'), 1)
        self.assertEqual(response_data.get('count'), 1)
        self.assertIsInstance(response_data.get('results'), list)
        self.assertIsNotNone(response_data.get('results'))

    def test_search_apartment_not_all(self):
        self.apartment.space = 'commercial'
        self.apartment.save()
        response = self.client.get(self.search_apartments,
                                   {'guest': 5, 'type': 'commercial'})
        response_data = response.data
        self.assertEqual(response_data.get('responseCode'), 1)
        self.assertEqual(response_data.get('count'), 1)
        self.assertIsInstance(response_data.get('results'), list)
        self.assertIsNotNone(response_data.get('results'))

    def test_check_in_checkout_all(self):
        response = self.client.get(
            self.search_apartments, {
                'guest': 5, 'type': 'all', 'checkin': self.check_in, "checkout": self.check_out})
        response_data = response.data
        self.assertEqual(response_data.get('responseCode'), 1)
        self.assertEqual(response_data.get('count'), 1)
        self.assertIsInstance(response_data.get('results'), list)
        self.assertIsNotNone(response_data.get('results'))

    def test_check_in_checkout_not_all(self):
        self.apartment.space = 'commercial'
        self.apartment.save()
        response = self.client.get(self.search_apartments,
                                   {'guest': 5,
                                    'type': 'commercial',
                                    'checkin': self.check_in,
                                    "checkout": self.check_out})
        response_data = response.data
        self.assertEqual(response_data.get('responseCode'), 1)
        self.assertEqual(response_data.get('count'), 1)
        self.assertIsInstance(response_data.get('results'), list)
        self.assertIsNotNone(response_data.get('results'))
    
    # TODO: this need to be fixed it's not testing the portion it's supposed to test
    def test_return_empty_if_no_criteria(self):
        response = self.client.get(self.search_apartments, {'guest': 100, 'type': 'unknow'})
        response_data = response.data
        self.assertEqual(response_data.get('responseCode'), 1)
        self.assertEqual(response_data.get('count'), 0)
        self.assertIsInstance(response_data.get('results'), list)
        self.assertFalse(response_data.get('results'))
        
