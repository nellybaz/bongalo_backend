from django.test import TestCase
from .factories import ApartmentFactory
from apartment.models import Apartment


class ApartmentTestCase(TestCase):
    def test_string_representation(self):
        """Test for string representation."""
        apartment = ApartmentFactory()
        self.assertEqual(str(apartment), apartment.title)
