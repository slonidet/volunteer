from users.models import User, Story
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import Profile, ProfileAttachment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_active', 'is_superuser', 'is_staff',
            'password', 'date_joined', 'last_login', 'profile',
            'profile_attachment'
        )
        read_only_fields = (
            'is_superuser', 'is_staff', 'last_login', 'date_joined', 'profile',
            'profile_attachment'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        if 'password' not in validated_data:
            raise serializers.ValidationError(
                {'password': _('Необходимо заполнить пароль')}
            )

        validated_data['password'] = make_password(validated_data['password'])
        instance = self._user_update_or_create(validated_data)

        return instance

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data['password'] = instance.password

        instance = self._user_update_or_create(validated_data, instance)

        return instance

    def _user_update_or_create(self, validated_data, instance=None):
        system_groups = validated_data.pop('system_groups', None)

        if instance:
            instance = super().update(instance, validated_data)
        else:
            instance = super().create(validated_data)

        system_groups_is_passed = (system_groups is not None)

        if system_groups_is_passed:
            self.set_user_groups(instance, system_groups)

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    benefits = serializers.MultipleChoiceField(
        choices=Profile.BENEFIT_CHOICES,
        label=Profile._meta.get_field('benefits').verbose_name,
    )

    class Meta:
        model = Profile
        fields = '__all__'

    def validate_benefits(self, value):
        if len(value) > 4:
            raise serializers.ValidationError(
                _('нельзя выбрать более 4-х значени')
            )

        return value


class ProfileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAttachment
        fields = '__all__'


class StoryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'age')


class AdminStorySerializer(serializers.ModelSerializer):
    profile = StoryProfileSerializer(read_only=True)
    profile_photo = serializers.ImageField(
        label='Фото', source='profile.user.profile_attachment.photo',
        read_only=True
    )

    class Meta:
        model = Story
        fields = '__all__'


class StorySerializer(AdminStorySerializer):
    class Meta(AdminStorySerializer.Meta):
        fields = ('text', 'about_yourself', 'profile', 'profile_photo')
