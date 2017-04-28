from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import (
    validate_password as validate
)
from django.db import IntegrityError
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from core.serializers import HyperlinkedSorlImageField
from core.translation_serializers import AdminTranslationMixin, \
    UserTranslationMixin
from permissions import GROUPS, GROUP_LEVEL
from users.models import Profile, ProfileAttachment, Story, StoryComment
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
        read_only_fields = ('status',)

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
        extra_kwargs = {'updated_at': {'read_only': False}}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
        extra_kwargs = {'name': {'validators': []}}


class BaseUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(label='Адрес электронной почты')

    _exclude_from_writable_fields = (
        'role', 'is_superuser', 'is_staff', 'last_login', 'date_joined'
    )

    @cached_property
    def _writable_fields(self):
        """ Exclude from writable fields """
        writable_fields = super()._writable_fields

        return [i for i in writable_fields
                if i.source not in self._exclude_from_writable_fields]


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
        read_only_fields = ('profile', 'profile_attachment', 'groups')
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

    _exclude_from_writable_fields = (
        'is_superuser', 'is_staff', 'last_login', 'date_joined'
    )

    class Meta(UserSerializer.Meta):
        read_only_fields = ('profile', 'profile_attachment')

    def validate_groups(self, groups):
        if groups:
            if len(groups) > 1:
                raise serializers.ValidationError(
                    _('Пользователь может состоять только в одной группе')
                )

            group_name = groups[0]['name']

            actor_groups = self.context['request'].user.groups.values_list(
                'name', flat=True
            )
            if actor_groups:
                actor_group_levels = [GROUP_LEVEL.get(g) for g in actor_groups]
                actor_group_level = max(actor_group_levels)
                if actor_group_level < GROUP_LEVEL.get(group_name):
                    raise serializers.ValidationError(
                        _('Можно устанавливать только группу более низкого '
                          'ранга чем собственная')
                    )

        return groups

    def update(self, user, validated_data):
        groups = validated_data.pop('groups', None)
        user = super().update(user, validated_data)

        if groups:
            group_name = groups[0]['name']
            group = Group.objects.get_by_natural_key(group_name)
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
    image = HyperlinkedSorlImageField(
        '600x400', options={'upscale': False}, required=False
    )
    thumbnail = HyperlinkedSorlImageField(
        '320x240', options={"crop": "center"},
        source='image', read_only=True
    )
    profile = StoryProfileSerializer(read_only=True)
    profile_photo = serializers.ImageField(
        label='Фото', source='profile.user.profile_attachment.photo',
        read_only=True
    )

    class Meta:
        model = Story
        model_translation = StoryTranslationOptions


class StoryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryComment
        fields = '__all__'


class AdminStorySerializer(AdminTranslationMixin, BaseStorySerializer):
    comments = StoryCommentSerializer(read_only=True, many=True)

    class Meta(BaseStorySerializer.Meta):
        fields = '__all__'


class StorySerializer(UserTranslationMixin, BaseStorySerializer):
    image = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta(BaseStorySerializer.Meta):
        fields = ['id', 'text', 'about_yourself', 'profile', 'image',
                  'thumbnail']

    def get_image(self, obj):
        return self._get_story_or_profile_image(obj, '600x400', upscale=False)

    def get_thumbnail(self, obj):
        return self._get_story_or_profile_image(obj, '320x240', options={"crop": "center"})

    def _get_story_or_profile_image(self, obj, geometry_string, **kwargs):
        try:
            obj = obj.image if obj.image \
                else obj.profile.user.profile_attachment.photo
        except ProfileAttachment.DoesNotExist:
            obj = None

        if not obj:
            return None

        image = get_thumbnail(obj, geometry_string, **kwargs)
        request = self.context.get('request')

        return request.build_absolute_uri(image.url)


class UserGroupSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'display_name',)
        read_only_fields = ('name',)

    def get_display_name(self, obj):
        return GROUPS.get(obj.name, '')


class ProfileCityProfessionSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('last_name', 'first_name', 'middle_name',
                  'residential_address', 'position',)
