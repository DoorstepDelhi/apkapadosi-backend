from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    location = models.PointField(geography=True, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_private = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    close_friends = models.ManyToManyField('self', symmetrical=False, related_name='close_friend_of', blank=True)
    favorite_entities = models.ManyToManyField('entities.Entity', related_name='favorited_by', blank=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_entity = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def set_location(self, longitude, latitude):
        self.location = Point(longitude, latitude)
        self.save()

    def add_friend(self, user):
        if user not in self.friends.all():
            self.friends.add(user)
            user.friends.add(self)

    def remove_friend(self, user):
        self.friends.remove(user)
        user.friends.remove(self)

    def follow(self, user):
        if user not in self.following.all():
            self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    def add_close_friend(self, user):
        if user not in self.close_friends.all():
            self.close_friends.add(user)

    def remove_close_friend(self, user):
        self.close_friends.remove(user)

    def block_user(self, user):
        if user not in self.blocked_users.all():
            self.blocked_users.add(user)
            self.friends.remove(user)
            self.following.remove(user)
            self.followers.remove(user)

    def unblock_user(self, user):
        self.blocked_users.remove(user)

class UserPreferences(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name='preferences')
    notification_email = models.BooleanField(default=True)
    notification_push = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    theme = models.CharField(max_length=20, default='light')
    preferred_categories = models.JSONField(default=list)
    notification_settings = models.JSONField(default=dict)
    search_radius = models.IntegerField(default=10)  # in kilometers

    def __str__(self):
        return f"{self.user}'s preferences"


class SocialMediaAccount(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='social_accounts')
    platform = models.CharField(max_length=50)
    account_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'platform')

    def __str__(self):
        return f"{self.user} - {self.platform}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'New Follower'),
        ('friend_request', 'Friend Request'),
        ('message', 'New Message'),
        ('comment', 'New Comment'),
        ('review', 'New Review'),
        ('like', 'New Like'),
        ('nearby_entity', 'Nearby Entity'),
        ('entity_update', 'Entity Update'),
        ('product_update', 'Product Update'),
        ('service_update', 'Service Update'),
    )

    recipient = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.recipient.username}"

    def mark_as_read(self):
        self.is_read = True
        self.save()
