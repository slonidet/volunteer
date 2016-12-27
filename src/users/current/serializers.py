from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.current.mixins import CurrentUserSerializerMixin
from users.models import Profile, ProfileAttachment
from users.serializers import User, UserSerializer, ProfileSerializer, \
    ProfileAttachmentSerializer, AdminStorySerializer


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


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'username', 'is_superuser', 'is_staff',
            'password', 'date_joined', 'last_login', 'profile',
            'profile_attachment'
        )
        read_only_fields = (
            'is_superuser', 'is_staff', 'last_login', 'date_joined', 'profile',
            'profile_attachment'
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


class CurrentUserProfileAttachmentSerializer(CurrentUserSerializerMixin,
                                             ProfileAttachmentSerializer):

    class Meta(CurrentUserSerializerMixin.Meta):
        model = ProfileAttachment


class CurrentUserStorySerializer(AdminStorySerializer):
    class Meta(AdminStorySerializer.Meta):
        fields = (
            'text', 'about_yourself', 'profile', 'admin_comment', 'is_public'
        )
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
