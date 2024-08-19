import unittest
from django.test import TestCase
from django.contrib.gis.geos import Point
from utils.geolocation import calculate_distance
from utils.validators import validate_entity, validate_listing
from subdomains.utils import generate_subdomain

class TestGeolocation(TestCase):
    def test_calculate_distance(self):
        point1 = Point(0, 0)
        point2 = Point(1, 1)
        distance = calculate_distance(point1, point2)
        self.assertAlmostEqual(distance, 157.2, places=1)

class TestValidators(TestCase):
    def test_validate_entity(self):
        valid_entity = {
            'name': 'Test Entity',
            'type': 'BUSINESS',
            'contact_email': 'test@example.com',
            'phone_number': '+1234567890'
        }
        self.assertTrue(validate_entity(valid_entity))

        invalid_entity = {
            'name': '',
            'type': 'INVALID_TYPE',
            'contact_email': 'invalid_email',
            'phone_number': '123'
        }
        self.assertFalse(validate_entity(invalid_entity))

    def test_validate_listing(self):
        valid_listing = {
            'title': 'Test Listing',
            'description': 'This is a test listing',
            'price': 100.00,
            'category': 'GOODS'
        }
        self.assertTrue(validate_listing(valid_listing))

        invalid_listing = {
            'title': '',
            'description': 'Short',
            'price': -10,
            'category': 'INVALID_CATEGORY'
        }
        self.assertFalse(validate_listing(invalid_listing))

class TestSubdomainUtils(TestCase):
    def test_generate_subdomain(self):
        entity_name = "Test Entity"
        subdomain = generate_subdomain(entity_name)
        self.assertEqual(subdomain, "test-entity")

        entity_name = "Test & Entity 123"
        subdomain = generate_subdomain(entity_name)
        self.assertEqual(subdomain, "test-entity-123")

if __name__ == '__main__':
    unittest.main()