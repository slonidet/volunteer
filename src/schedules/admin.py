from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from schedules.models import Place, Position, Shift, Period, Day, \
    UserPosition, Team


class PositionInline(admin.TabularInline):
    model = Position


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [PositionInline]


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'functionality', 'place')
    list_filter = ('place',)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class DayInline(admin.TabularInline):
    model = Day


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [DayInline]


class DayAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'date')
    list_filter = ('period',)


class UserPositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'user', 'team', 'shift', 'is_permanent')
    list_filter = (
        'position__place', 'position__functionality', 'team', 'shift',
        'is_permanent'
    )


class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'place', 'get_team_leader', 'shift', 'period'
    )
    list_filter = ('place', 'shift', 'period')
    readonly_fields = ('members', )

    def get_team_leader(self, obj):
        return getattr(obj.team_leader_position, 'user', None)

    get_team_leader.short_description = _('Старший волонтёр')
    get_team_leader.admin_order_field = 'team_leader_position__user'


admin.site.register(Place, PlaceAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(UserPosition, UserPositionAdmin)
admin.site.register(Team, TeamAdmin)
