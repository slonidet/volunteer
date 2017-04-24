from django.contrib import admin
from users.models import User, Story
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, \
    UserChangeForm as BaseUserChangeForm, \
    UserCreationForm as BaseUserCreationForm
from import_export.admin import ImportExportActionModelAdmin

from .models import Profile, ProfileAttachment
from .admin_resources import ProfileAdminResource


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        readonly_fields = ('role',)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Права доступа'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups',
            'user_permissions'
        )}),
        (_('События'), {'fields': ('last_login', 'date_joined')}),
        (_('Остальное'), {'fields': ('role',)}),
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
    list_display = ('username', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_display = (
        'id', 'username', 'is_active', 'is_staff', 'role', 'date_joined'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'role')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [ProfileInline]


class ProfileAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'gender',
                    'status')
    list_filter = ('status', 'gender', 'user__role',)

    def get_export_resource_class(self):
        return ProfileAdminResource


class ProfileAttachmentAdmin(admin.ModelAdmin):
    pass


class StoryAdmin(TranslationAdmin):
    list_display = ('id', 'is_public')
    list_filter = ('is_public',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileAttachment, ProfileAttachmentAdmin)
admin.site.register(Story, StoryAdmin)
