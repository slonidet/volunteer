from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import Profile, ProfileAttachment
from users.serializers import User, UserSerializer, ProfileSerializer


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


class CurrentUserProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        exclude = ('user', )

    # def validate_user(self, value):
    #     try:
    #         user = self.context['request'].user
    #     except KeyError:
    #         return value
    #
    #     if not user.is_superuser and value != user:
    #         raise serializers.ValidationError(
    #             _('нельзя изменять анкеты других пользоватетей'))
    #
    #     return value


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
