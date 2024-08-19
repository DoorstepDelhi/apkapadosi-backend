import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from entities.models import Entity, Listing
from users.models import User
from reviews.models import Review
from media.models import Media

User = get_user_model()

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        url = reverse('user-list')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_profile_retrieval(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

class EntityViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='entityowner@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.entity_data = {
            'name': 'Test Entity',
            'type': 'BUSINESS',
            'description': 'A test entity',
            'location': Point(1.0, 1.0)
        }
        self.entity = Entity.objects.create(owner=self.user, **self.entity_data)

    def test_entity_creation(self):
        url = reverse('entity-list')
        data = {
            'name': 'New Entity',
            'type': 'INDIVIDUAL',
            'description': 'A new test entity',
            'location': json.dumps({'type': 'Point', 'coordinates': [2.0, 2.0]})
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entity.objects.count(), 2)

    def test_entity_retrieval(self):
        url = reverse('entity-detail', kwargs={'pk': self.entity.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.entity_data['name'])

class ListingViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='listingowner@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.entity = Entity.objects.create(owner=self.user, name='Test Entity', type='BUSINESS', location=Point(1.0, 1.0))
        self.listing_data = {
            'title': 'Test Listing',
            'description': 'A test listing',
            'price': '100.00',
            'category': 'GOODS',
            'location': Point(1.1, 1.1)
        }
        self.listing = Listing.objects.create(entity=self.entity, **self.listing_data)

    def test_listing_creation(self):
        url = reverse('listing-list')
        data = {
            'title': 'New Listing',
            'description': 'A new test listing',
            'price': '200.00',
            'category': 'SERVICES',
            'location': json.dumps({'type': 'Point', 'coordinates': [2.1, 2.1]}),
            'entity': self.entity.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.count(), 2)

    def test_listing_retrieval(self):
        url = reverse('listing-detail', kwargs={'pk': self.listing.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.listing_data['title'])

class SearchViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='searchuser@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.entity = Entity.objects.create(owner=self.user, name='Search Entity', type='BUSINESS', location=Point(1.0, 1.0))
        self.listing = Listing.objects.create(
            entity=self.entity,
            title='Searchable Listing',
            description='A listing to be searched',
            price='150.00',
            category='GOODS',
            location=Point(1.1, 1.1)
        )

    def test_geolocation_search(self):
        url = reverse('search-listings')
        data = {
            'latitude': 1.0,
            'longitude': 1.0,
            'radius': 10  # km
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.listing.title)

    def test_keyword_search(self):
        url = reverse('search-listings')
        data = {
            'keyword': 'Searchable'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.listing.title)

class ReviewViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='reviewer@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.entity = Entity.objects.create(owner=self.user, name='Reviewed Entity', type='BUSINESS', location=Point(1.0, 1.0))
        self.review_data = {
            'rating': 4,
            'comment': 'Great service!',
            'entity': self.entity.pk
        }

    def test_review_creation(self):
        url = reverse('review-list')
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().rating, 4)

    def test_review_retrieval(self):
        review = Review.objects.create(user=self.user, **self.review_data)
        url = reverse('review-detail', kwargs={'pk': review.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], self.review_data['comment'])

class MediaViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='mediaowner@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.entity = Entity.objects.create(owner=self.user, name='Media Entity', type='BUSINESS', location=Point(1.0, 1.0))
        self.listing = Listing.objects.create(
            entity=self.entity,
            title='Media Listing',
            description='A listing with media',
            price='300.00',
            category='SERVICES',
            location=Point(1.2, 1.2)
        )
        self.media_data = {
            'type': 'IMAGE',
            'file': 'path/to/image.jpg',
            'listing': self.listing.pk
        }

    def test_media_upload(self):
        url = reverse('media-list')
        response = self.client.post(url, self.media_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Media.objects.count(), 1)
        self.assertEqual(Media.objects.first().type, 'IMAGE')

    def test_media_retrieval(self):
        media = Media.objects.create(**self.media_data)
        url = reverse('media-detail', kwargs={'pk': media.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file'], self.media_data['file'])