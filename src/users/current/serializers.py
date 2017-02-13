from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from core.serializers import HyperlinkedSorlImageField
from users.current.mixins import CurrentUserSerializerMixin
from users.models import Profile, ProfileAttachment
from users.serializers import User, UserSerializer, ProfileSerializer, \
    ProfileAttachmentSerializer, StorySerializer, BaseUserSerializer


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


class AuthGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class AuthUserSerializer(BaseUserSerializer):
    profile = AuthProfileSerializer(read_only=True)
    profile_attachment = AuthProfileAttachmentSerializer(read_only=True)
    groups = AuthGroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_superuser', 'profile', 'profile_attachment',
            'role', 'groups',
        )


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'username', 'is_superuser', 'is_staff',
            'password', 'date_joined', 'last_login', 'profile',
            'profile_attachment', 'groups', 'role'
        )
        read_only_fields = (
            'is_superuser', 'is_staff', 'last_login', 'date_joined', 'profile',
            'profile_attachment', 'groups', 'role'
        )

    def update(self, instance, validated_data):
        try_change_username = (
            'username' in validated_data and
            instance.username != validated_data['username']
        )
        if try_change_username:
            raise serializers.ValidationError(
                {'username': _('Нельзя изменять email пользователя')}
            )

        return super().update(instance, validated_data)


class CurrentUserProfileSerializer(CurrentUserSerializerMixin,
                                   ProfileSerializer):

    class Meta(CurrentUserSerializerMixin.Meta):
        model = Profile
        read_only_fields = ('status', )


class CurrentUserProfileAttachmentSerializer(CurrentUserSerializerMixin,
                                             ProfileAttachmentSerializer):

    class Meta(CurrentUserSerializerMixin.Meta):
        model = ProfileAttachment


class CurrentUserStorySerializer(StorySerializer):
    image = HyperlinkedSorlImageField(
        '600x400', options={'upscale': False}, required=False
    )
    thumbnail = HyperlinkedSorlImageField(
        '320x240', options={"crop": "center"},
        source='image', read_only=True
    )

    class Meta(StorySerializer.Meta):
        fields = [
            'id', 'text', 'about_yourself', 'admin_comment', 'is_public',
            'image', 'thumbnail',
        ]
        read_only_fields = ('is_public', 'admin_comment')

    def create(self, validated_data):
        try:
            profile = Profile.objects.get(user=self.context['request'].user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {'profile': _('Необходимо заполнить анкету')}
            )
        validated_data['profile'] = profile

        return super().create(validated_data)
