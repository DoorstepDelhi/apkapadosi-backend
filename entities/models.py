from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from utils.validators import validate_coordinates, validate_phone_number, validate_website_url, validate_image_file, validate_document_file

class Entity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.PointField(validators=[validate_coordinates])
    address = models.TextField()
    contact_info = models.CharField(max_length=255, validators=[validate_phone_number])
    email = models.EmailField()
    website = models.URLField(blank=True, null=True, validators=[validate_website_url])
    logo = models.ImageField(upload_to='entity_logos/', blank=True, null=True, validators=[validate_image_file])
    documents = ArrayField(models.FileField(upload_to='entity_documents/', validators=[validate_document_file]), blank=True, null=True)
    deals_in = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    business_hours = models.JSONField(default=dict, blank=True, null=True)
    amenities = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    payment_methods = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    social_media_links = models.JSONField(default=dict, blank=True, null=True)
    additional_info = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.name

class EntityUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('collaborator', 'Collaborator'),
    ]
    PERMISSION_CHOICES = [
        ('edit', 'Edit'),
        ('view', 'View'),
    ]

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, null=True, blank=True)
    is_creator = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('entity', 'user')

    def __str__(self):
        return f"{self.user.get_username()} - {self.role.capitalize()} of {self.entity.name}"

class EntityMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('tour_360', '360 Tour'),
    ]

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='entity_media/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_media_type_display()} for {self.entity.name}"