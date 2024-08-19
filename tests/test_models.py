import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
# from entities.models import Entity, Listing
# from reviews.models import Review
# from media.models import Media
# from analytics.models import Analytics

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.get_full_name(), 'Test User')


# class EntityModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='entity@example.com',
#             password='entitypassword123'
#         )
#         self.entity = Entity.objects.create(
#             user=self.user,
#             name='Test Entity',
#             entity_type='BUSINESS',
#             location=Point(1.0, 1.0)
#         )

#     def test_entity_creation(self):
#         self.assertTrue(isinstance(self.entity, Entity))
#         self.assertEqual(self.entity.name, 'Test Entity')
#         self.assertEqual(self.entity.entity_type, 'BUSINESS')
#         self.assertEqual(self.entity.location, Point(1.0, 1.0))

# class ListingModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='entity@example.com',
#             password='entitypassword123'
#         )
#         self.entity = Entity.objects.create(
#             user=self.user,
#             name='Test Entity',
#             entity_type='BUSINESS',
#             location=Point(1.0, 1.0)
#         )
#         self.listing = Listing.objects.create(
#             entity=self.entity,
#             title='Test Listing',
#             description='This is a test listing',
#             price=100.00,
#             category='GOODS'
#         )

#     def test_listing_creation(self):
#         self.assertTrue(isinstance(self.listing, Listing))
#         self.assertEqual(self.listing.title, 'Test Listing')
#         self.assertEqual(self.listing.price, 100.00)
#         self.assertEqual(self.listing.category, 'GOODS')


# class ReviewModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='user@example.com',
#             password='userpassword123'
#         )
#         self.entity = Entity.objects.create(
#             user=self.user,
#             name='Test Entity',
#             entity_type='BUSINESS',
#             location=Point(1.0, 1.0)
#         )
#         self.review = Review.objects.create(
#             user=self.user,
#             entity=self.entity,
#             rating=4,
#             comment='Great service!'
#         )

#     def test_review_creation(self):
#         self.assertTrue(isinstance(self.review, Review))
#         self.assertEqual(self.review.rating, 4)
#         self.assertEqual(self.review.comment, 'Great service!')


# class MediaModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='entity@example.com',
#             password='entitypassword123'
#         )
#         self.entity = Entity.objects.create(
#             user=self.user,
#             name='Test Entity',
#             entity_type='BUSINESS',
#             location=Point(1.0, 1.0)
#         )
#         self.media = Media.objects.create(
#             entity=self.entity,
#             media_type='3D_TOUR',
#             file_path='/media/3d_tours/test_tour.glb'
#         )

#     def test_media_creation(self):
#         self.assertTrue(isinstance(self.media, Media))
#         self.assertEqual(self.media.media_type, '3D_TOUR')
#         self.assertEqual(self.media.file_path, '/media/3d_tours/test_tour.glb')


# class AnalyticsModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='entity@example.com',
#             password='entitypassword123'
#         )
#         self.entity = Entity.objects.create(
#             user=self.user,
#             name='Test Entity',
#             entity_type='BUSINESS',
#             location=Point(1.0, 1.0)
#         )
#         self.analytics = Analytics.objects.create(
#             entity=self.entity,
#             views=100,
#             clicks=50,
#             conversions=10
#         )

#     def test_analytics_creation(self):
#         self.assertTrue(isinstance(self.analytics, Analytics))
#         self.assertEqual(self.analytics.views, 100)
#         self.assertEqual(self.analytics.clicks, 50)
#         self.assertEqual(self.analytics.conversions, 10)

if __name__ == '__main__':
    unittest.main()