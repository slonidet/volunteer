from django.contrib import admin
from users.models import User, Story
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin, UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm,
)

from users.models import Profile, ProfileAttachment


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2',
            ),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


class ProfileAdmin(admin.ModelAdmin):
    pass


class ProfileAttachmentAdmin(admin.ModelAdmin):
    pass


class StoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileAttachment, ProfileAttachmentAdmin)
admin.site.register(Story, StoryAdmin)
