from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from .models import UserPreferences, SocialMediaAccount, Notification

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_fields(self):
        self.user.phone_number = '1234567890'
        self.user.date_of_birth = '1990-01-01'
        self.user.bio = 'Test bio'
        self.user.location = Point(1, 1)
        self.user.is_entity = True
        self.user.save()

        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(str(self.user.date_of_birth), '1990-01-01')
        self.assertEqual(self.user.bio, 'Test bio')
        self.assertEqual(self.user.location, Point(1, 1))
        self.assertTrue(self.user.is_entity)

class UserPreferencesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.preferences = UserPreferences.objects.create(
            user=self.user,
            preferred_categories=['category1', 'category2'],
            notification_settings={'email': True, 'push': False},
            search_radius=20
        )

    def test_user_preferences_creation(self):
        self.assertTrue(isinstance(self.preferences, UserPreferences))
        self.assertEqual(self.preferences.user, self.user)

    def test_user_preferences_str_representation(self):
        self.assertEqual(str(self.preferences), "testuser's preferences")

    def test_user_preferences_fields(self):
        self.assertEqual(self.preferences.preferred_categories, ['category1', 'category2'])
        self.assertEqual(self.preferences.notification_settings, {'email': True, 'push': False})
        self.assertEqual(self.preferences.search_radius, 20)

class SocialMediaAccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.social_account = SocialMediaAccount.objects.create(
            user=self.user,
            platform='facebook',
            account_id='12345',
            access_token='token123'
        )

    def test_social_media_account_creation(self):
        self.assertTrue(isinstance(self.social_account, SocialMediaAccount))
        self.assertEqual(self.social_account.user, self.user)

    def test_social_media_account_str_representation(self):
        self.assertEqual(str(self.social_account), 'testuser - facebook')

    def test_social_media_account_unique_together(self):
        with self.assertRaises(ValidationError):
            SocialMediaAccount.objects.create(
                user=self.user,
                platform='facebook',
                account_id='67890',
                access_token='token456'
            )

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type='message',
            content='Test notification'
        )

    def test_notification_creation(self):
        self.assertTrue(isinstance(self.notification, Notification))
        self.assertEqual(self.notification.recipient, self.user)

    def test_notification_str_representation(self):
        self.assertEqual(str(self.notification), 'New Message for testuser')

    def test_notification_mark_as_read(self):
        self.assertFalse(self.notification.is_read)
        self.notification.mark_as_read()
        self.assertTrue(self.notification.is_read)

    def test_notification_ordering(self):
        notification2 = Notification.objects.create(
            recipient=self.user,
            notification_type='follow',
            content='Test notification 2'
        )
        notifications = Notification.objects.all()
        self.assertEqual(notifications[0], notification2)
        self.assertEqual(notifications[1], self.notification)
