from django.contrib import admin

from user_tests.models import Test, UserTest


class UserAdmin(admin.ModelAdmin):
    pass


class TestAdmin(admin.ModelAdmin):
    pass


class UserTestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Test, TestAdmin)
admin.site.register(UserTest, UserTestAdmin)


