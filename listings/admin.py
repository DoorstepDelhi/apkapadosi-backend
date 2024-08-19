from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import Category, Listing, ListingImage, Service, Event, Review, Collection

class ListingImageInline(NestedTabularInline):
    model = ListingImage
    extra = 1

class ServiceInline(NestedTabularInline):
    model = Service

class EventInline(NestedTabularInline):
    model = Event

class ReviewInline(NestedTabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'review_text', 'review_date', 'is_verified_purchase')

@admin.register(Listing)
class ListingAdmin(NestedModelAdmin):
    inlines = [ListingImageInline, ServiceInline, EventInline, ReviewInline]
    list_display = ('title', 'vendor', 'category', 'price', 'listing_type', 'availability_status', 'listing_date', 'is_featured')
    list_filter = ('listing_type', 'condition', 'availability_status', 'is_featured', 'listing_date')
    search_fields = ('title', 'description', 'vendor__name')
    readonly_fields = ('views', 'listing_date')
    fieldsets = (
        (None, {'fields': ('vendor', 'category', 'title', 'description', 'price')}),
        ('Listing Details', {'fields': ('listing_type', 'condition', 'availability_status', 'location')}),
        ('Dates', {'fields': ('listing_date', 'expiry_date')}),
        ('Statistics', {'fields': ('views', 'is_featured')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent_category')
    search_fields = ('category_name',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity', 'created_at', 'updated_at')
    filter_horizontal = ('listings',)
    search_fields = ('name', 'entity__name')
    readonly_fields = ('created_at', 'updated_at')
