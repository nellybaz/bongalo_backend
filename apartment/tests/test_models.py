from django.test import TestCase
from .factories import ApartmentFactory, ApartmentWithImagesFactory
from apartment.models import Apartment, Images


class ApartmentTestCase(TestCase):
    def test_string_representation(self):
        """Test for string representation."""
        apartment = ApartmentFactory()
        self.assertEqual(str(apartment), apartment.title)

    def test_create_apartment_with_images(self):
        apartment = ApartmentWithImagesFactory.create(images=5)
        self.assertIsInstance(apartment, Apartment)
        images = apartment.images.all()
        self.assertTrue(len(images) == 5)
        for image in images:
            self.assertIsInstance(image, Images)
