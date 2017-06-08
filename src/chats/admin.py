from django.contrib import admin

from chats.models import Room, Message


class RoomAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
