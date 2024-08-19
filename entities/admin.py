from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import Entity, EntityUser, EntityMedia

class EntityUserInline(NestedTabularInline):
    model = EntityUser
    extra = 1

class EntityMediaInline(NestedTabularInline):
    model = EntityMedia
    extra = 1

@admin.register(Entity)
class EntityAdmin(NestedModelAdmin, gis_admin.OSMGeoAdmin):
    inlines = [EntityUserInline, EntityMediaInline]
    list_display = ('name', 'email', 'contact_info', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'contact_info')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'location', 'address')}),
        ('Contact Information', {'fields': ('contact_info', 'email', 'website')}),
        ('Media', {'fields': ('logo',)}),
        ('Business Details', {'fields': ('deals_in', 'documents', 'business_hours', 'amenities', 'payment_methods')}),
        ('Social Media', {'fields': ('social_media_links',)}),
        ('Additional Information', {'fields': ('additional_info',)}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

@admin.register(EntityUser)
class EntityUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'entity', 'role', 'permission', 'is_creator', 'created_at')
    list_filter = ('role', 'permission', 'is_creator', 'created_at')
    search_fields = ('user__username', 'entity__name')
    readonly_fields = ('created_at',)

@admin.register(EntityMedia)
class EntityMediaAdmin(admin.ModelAdmin):
    list_display = ('entity', 'media_type', 'created_at')
    list_filter = ('media_type', 'created_at')
    search_fields = ('entity__name',)
    readonly_fields = ('created_at',)
