from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import Profile, ProfileAttachment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_superuser', 'is_staff', 'password',
            'date_joined', 'last_login', 'profile', 'profile_attachment'
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
        try_change_username = (
            'username' in validated_data and
            instance.username != validated_data['username']
        )
        if try_change_username:
            raise serializers.ValidationError(
                {'username': _('Нельзя изменять email пользователя')}
            )

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

    def validate_user(self, value):
        try:
            user = self.context['request'].user
        except KeyError:
            return value

        if not user.is_superuser and value != user:
            raise serializers.ValidationError(
                _('нельзя изменять анкеты других пользоватетей'))

        return value

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

    def validate_user(self, value):
        try:
            user = self.context['request'].user
        except KeyError:
            return value

        if not user.is_superuser and value != user:
            raise serializers.ValidationError(
                _('нельзя изменять фото других пользоватетей'))

        return value


