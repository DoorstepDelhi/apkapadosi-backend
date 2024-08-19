from django.contrib.gis.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    LISTING_TYPES = [
        ('product', 'Product'),
        ('service', 'Service'),
        ('event', 'Event'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
    ]

    vendor = models.ForeignKey('entities.Entity', on_delete=models.CASCADE)
    category = models.ForeignKey("listings.Category", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    availability_status = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES)
    location = models.PointField()
    listing_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey("listings.Listing", on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='listing_images/')
    image_alt_text = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"

class Service(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, primary_key=True)
    service_type = models.CharField(max_length=100)
    service_duration = models.DurationField()
    service_area = models.CharField(max_length=255)
    service_provider_details = models.TextField()

    def __str__(self):
        return f"Service: {self.listing.title}"

class Event(models.Model):
    listing = models.OneToOneField("listings.Listing", on_delete=models.CASCADE, primary_key=True)
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    event_description = models.TextField()
    tickets_available = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.event_name

class Review(models.Model):
    listing = models.ForeignKey("listings.Listing", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    is_verified_purchase = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.listing.title} by {self.user.username}"

class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    entity = models.ForeignKey('entities.Entity', on_delete=models.CASCADE, related_name='collections')
    listings = models.ManyToManyField(Listing, related_name='collections', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
