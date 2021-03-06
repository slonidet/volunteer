from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.current.mixins import CurrentUserSerializerMixin
from users.models import Profile, ProfileAttachment
from users.serializers import User, UserSerializer, ProfileSerializer, \
    ProfileAttachmentSerializer, BaseUserSerializer, BaseStorySerializer, \
    AdminStorySerializer, StoryCommentSerializer


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
            'id', 'username', 'profile', 'profile_attachment', 'role',
            'groups',
        )


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'username', 'password', 'date_joined', 'last_login',
            'profile', 'profile_attachment', 'groups', 'role'
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
    class Meta(ProfileSerializer.Meta):
        pass


class CurrentUserProfileAttachmentSerializer(CurrentUserSerializerMixin,
                                             ProfileAttachmentSerializer):
    class Meta:
        model = ProfileAttachment
        fields = '__all__'


class CurrentUserStorySerializer(AdminStorySerializer):
    comments = StoryCommentSerializer(read_only=True, many=True)

    class Meta(BaseStorySerializer.Meta):
        fields = '__all__'
        read_only_fields = ('is_public',)

    def create(self, validated_data):
        try:
            profile = Profile.objects.get(user=self.context['request'].user)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {'profile': _('Необходимо заполнить анкету')}
            )
        validated_data['profile'] = profile

        return super().create(validated_data)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
