from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import (
    validate_password as validate
)
from django.db import IntegrityError
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from core.translation_serializers import AdminTranslationMixin, \
    UserTranslationMixin
from users.models import Profile, ProfileAttachment, Story
from users.models import User, ProfileComment
from users.translation import StoryTranslationOptions


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


class SimpleProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ('id', 'first_name', 'last_name', 'middle_name')


class ApproveProfileSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ('id', 'updated_at', 'status')
        read_only_fields = ('status', )
        extra_kwargs = {'updated_at': {'read_only': False}}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
        extra_kwargs = {'name': {'validators': []}}


class BaseUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(label='Адрес электронной почты')

    @cached_property
    def _writable_fields(self):
        """ Exclude role from writable fields """
        writable_fields = super()._writable_fields
        try:
            writable_fields.remove('role')
        except ValueError:
            pass

        return writable_fields


class SimpleUserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name')


class UserSerializer(BaseUserSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    profile = SimpleProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_active', 'password', 'date_joined',
            'last_login', 'profile', 'profile_attachment', 'groups', 'role',
        )
        read_only_fields = (
            'is_superuser', 'is_staff', 'last_login', 'date_joined', 'profile',
            'profile_attachment', 'groups', 'role',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def validate_password(self, password):
        validate(password)

        return password

    def create(self, validated_data):
        if 'password' not in validated_data:
            raise serializers.ValidationError(
                {'password': _('Необходимо заполнить пароль')}
            )

        validated_data['password'] = make_password(validated_data['password'])
        user = self._user_update_or_create(validated_data)

        return user

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
            try:
                instance = super().create(validated_data)
            except IntegrityError:
                raise serializers.ValidationError(
                    _('Пользователь с таким email уже существует, '
                      'проверьте почту для активации')
                )

        system_groups_is_passed = (system_groups is not None)

        if system_groups_is_passed:
            self.set_user_groups(instance, system_groups)

        return instance


class AdminUserSerializer(UserSerializer):
    groups = GroupSerializer(many=True, required=False)

    class Meta(UserSerializer.Meta):
        read_only_fields = (
            'is_superuser', 'is_staff', 'last_login', 'date_joined', 'profile',
            'profile_attachment', 'role',
        )

    def update(self, user, validated_data):
        groups = validated_data.pop('groups', None)
        user = super().update(user, validated_data)

        if groups:
            if len(groups) > 1:
                raise serializers.ValidationError(
                    _('Пользователь может состоять только в одной группе')
                )
            group = Group.objects.get_by_natural_key(groups[0]['name'])
            user.groups.set([group])

        return user


class ProfileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAttachment
        fields = '__all__'


class ProfileCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileComment
        fields = '__all__'


class StoryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'age')


class BaseStorySerializer(serializers.ModelSerializer):
    profile = StoryProfileSerializer(read_only=True)
    profile_photo = serializers.ImageField(
        label='Фото', source='profile.user.profile_attachment.photo',
        read_only=True
    )

    class Meta:
        model = Story
        model_translation = StoryTranslationOptions


class AdminStorySerializer(AdminTranslationMixin, BaseStorySerializer):
    class Meta(BaseStorySerializer.Meta):
        fields = '__all__'


class StorySerializer(UserTranslationMixin, BaseStorySerializer):
    class Meta(BaseStorySerializer.Meta):
        fields = ['id', 'text', 'about_yourself', 'profile', 'profile_photo']


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)
        read_only_fields = ('name',)
