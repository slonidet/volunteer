from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'last_login', 'is_superuser', 'username', 'is_staff',
            'is_active', 'date_joined', 'profile', 'password',
        )
        read_only_fields = (
            'is_superuser', 'is_staff', 'last_login', 'date_joined', 'profile'
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


class UserRegistrationSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = (
            'is_active', 'is_superuser', 'is_staff', 'last_login',
            'date_joined', 'profile'
        )


class ProfileSerializer(serializers.ModelSerializer):
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
                _('Нельзя изменять анкеты других пользоватетей'))

        return value


class AuthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('photo', 'first_name', 'last_name', 'gender', 'birthday')


class AuthUserSerializer(serializers.ModelSerializer):
    profile = AuthProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'profile')
