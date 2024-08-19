from rest_framework import serializers
from .models import Category, Listing, ListingImage, Service, Event, Review, Collection

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'parent_category']

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'listing', 'image_url', 'image_alt_text', 'upload_date']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['listing', 'service_type', 'service_duration', 'service_area', 'service_provider_details']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['listing', 'event_name', 'event_date', 'event_time', 'event_location', 'event_description', 'tickets_available', 'ticket_price']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'listing', 'user', 'rating', 'review_text', 'review_date', 'is_verified_purchase']

class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    service = ServiceSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'vendor', 'category', 'title', 'description', 'price', 'listing_type', 'condition', 'availability_status', 'location', 'listing_date', 'expiry_date', 'views', 'is_featured', 'images', 'service', 'event', 'reviews']

class CollectionSerializer(serializers.ModelSerializer):
    listings = ListingSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'entity', 'listings', 'created_at', 'updated_at']
