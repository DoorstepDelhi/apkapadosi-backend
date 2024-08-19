from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Notification, UserPreferences, SocialMediaAccount

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'location', 'bio', 'birth_date', 'phone_number', 'is_private', 'is_entity', 'profile_picture', 'created_at', 'updated_at')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=validated_data.get('bio', ''),
            birth_date=validated_data.get('birth_date'),
            phone_number=validated_data.get('phone_number', ''),
            is_private=validated_data.get('is_private', False),
            is_entity=validated_data.get('is_entity', False),
            profile_picture=validated_data.get('profile_picture')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'location', 'bio', 'birth_date', 'phone_number', 'is_private', 'is_entity', 'profile_picture', 'created_at', 'updated_at')
        read_only_fields = ('email', 'created_at', 'updated_at')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'recipient', 'notification_type', 'content', 'is_read', 'created_at', 'related_object_id', 'related_object_type']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.notification_type in ['friend_request', 'message']:
            representation.pop('related_object_id', None)
            representation.pop('related_object_type', None)
        elif instance.notification_type in ['entity_update', 'product_update', 'service_update']:
            representation.pop('sender', None)
        return representation

class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['recipient', 'notification_type', 'content', 'related_object_id', 'related_object_type']

    def create(self, validated_data):
        sender = self.context['request'].user
        notification = Notification.objects.create(sender=sender, **validated_data)
        return notification

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['notification_email', 'notification_push', 'language', 'theme', 'preferred_categories', 'notification_settings', 'search_radius']

class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccount
        fields = ['platform', 'account_id', 'access_token']
        extra_kwargs = {'access_token': {'write_only': True}}
