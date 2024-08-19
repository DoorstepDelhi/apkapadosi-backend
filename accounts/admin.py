from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import User, UserPreferences, SocialMediaAccount

class SocialMediaAccountInline(NestedTabularInline):
    model = SocialMediaAccount
    extra = 1

class UserPreferencesInline(NestedTabularInline):
    model = UserPreferences
    extra = 1

@admin.register(User)
class UserAdmin(NestedModelAdmin):
    inlines = [UserPreferencesInline, SocialMediaAccountInline]
    list_display = ('username', 'email', 'is_entity', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_entity', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'bio')}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
        ('Location', {'fields': ('location',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(UserPreferences)
admin.site.register(SocialMediaAccount)
