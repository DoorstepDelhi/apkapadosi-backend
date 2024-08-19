from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Entity, EntityUser, EntityMedia

class EntityUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityUser
        fields = ['id', 'user', 'role', 'permission', 'is_creator']

class EntityMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityMedia
        fields = ['id', 'media_type', 'file', 'url']

class EntitySerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    users = EntityUserSerializer(many=True, read_only=True)
    media = EntityMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'location', 'address', 'contact_info', 'email', 'website', 'logo', 'documents', 'deals_in', 'is_active', 'users', 'media', 'business_hours', 'amenities', 'payment_methods', 'social_media_links', 'additional_info']

    def get_location(self, obj):
        if obj.location:
            return {'latitude': obj.location.y, 'longitude': obj.location.x}
        return None

    def create(self, validated_data):
        location_data = validated_data.pop('location', None)
        
        if location_data:
            validated_data['location'] = Point(location_data['longitude'], location_data['latitude'])

        entity = Entity.objects.create(**validated_data)
        return entity

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        
        if location_data:
            instance.location = Point(location_data['longitude'], location_data['latitude'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class EntityListSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True)

    class Meta:
        model = Entity
        fields = ['id', 'name', 'description', 'location', 'distance']