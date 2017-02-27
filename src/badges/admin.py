from django.contrib import admin

from badges.models import Badge


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type')
    list_filter = ('type',)

admin.site.register(Badge, BadgeAdmin)
