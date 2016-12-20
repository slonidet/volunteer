from rest_framework import serializers

from users.models import Profile, ProfileAttachment
from users.serializers import User


class AuthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id', 'first_name', 'last_name', 'gender', 'birthday'
        )


class AuthProfileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAttachment
        fields = '__all__'


class AuthUserSerializer(serializers.ModelSerializer):
    profile = AuthProfileSerializer(read_only=True)
    profile_attachment = AuthProfileAttachmentSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_superuser', 'profile', 'profile_attachment'
        )