from django.test import TestCase
from apartment.serializers import ApartmentSerializer
from .factories import ApartmentWithImagesFactory
from rest_framework.serializers import ValidationError
from .utils import apartment_field_names


class ApartmentSerializersTest(TestCase):

    def setUp(self):
        self.apartment = ApartmentWithImagesFactory.create(images=5)
        self.serializer = ApartmentSerializer(instance=self.apartment)

    def test_apartment_serializer(self):
        """ test if all field in the models are in the serializers"""
        data = self.serializer.data
        field_names = apartment_field_names
        for field in field_names:
            self.assertEqual(
                str(data.get(field)),
                str(getattr(self.apartment, field))
            )
        self.assertCountEqual(data.keys(), field_names)

    def test_can_validate_owner(self):
        owner = self.serializer.validate_owner(self.apartment.owner.uuid)
        self.assertEqual(owner, self.apartment.owner.uuid)

    def test_raise_an_error_if_no_owner(self):
        with self.assertRaisesMessage(ValidationError, "user does not exists"):
            self.serializer.validate_owner('a-fake-owner')

    def test_can_update_apartment(self):
        data = {'title': 'this is an awesome',
                'description': 'I want to create something',
                'price': 1000}
        updated_apartment = self.serializer.update(
            self.apartment, data)
        for key in data.keys():
            self.assertEqual(getattr(updated_apartment, key), data.get(key))
