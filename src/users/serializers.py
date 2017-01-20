from django.contrib.auth.models import Group

from core.translation_serializers import AdminTranslationMixin, \
    UserTranslationMixin
from users.models import User, Story, ProfileComment
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import Profile, ProfileAttachment
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


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    profile = SimpleProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'is_active', 'is_superuser', 'is_staff',
            'password', 'date_joined', 'last_login', 'profile',
            'profile_attachment', 'groups'
        )
        read_only_fields = (
            'is_superuser', 'is_staff', 'last_login', 'date_joined', 'profile',
            'profile_attachment', 'groups'
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


class SimpleUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(label='Адрес электронной почты')

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name')


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


class UserGroupSerializer(UserTranslationMixin, BaseStorySerializer):
    users = SimpleUserSerializer(source='user_set', many=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'users')
        read_only_fields = ('name', )

    def create(self, validated_data):
        users = validated_data.pop('user_set', None)
        instance = super().create(validated_data)

        if users is not None:
            self.add_user_to_group(instance)

        return instance

    def update(self, instance, validated_data):
        users = validated_data.pop('user_set', None)
        instance = super().update(instance, validated_data)

        if users is not None:
            self.add_user_to_group(instance)

        return instance

    def add_user_to_group(self, group):
        user_ids = [u['id'] for u in self.initial_data['users']]
        users = User.objects.filter(pk__in=user_ids)
        group.user_set.set(users)
