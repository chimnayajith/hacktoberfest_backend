from django.contrib import admin

from attendance.models import Attendee, Attendance, Session

admin.site.register(Session)

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'roll_no', 'gender', 'email')

    search_fields = ('name', 'email')
    list_filter = ('gender',)

admin.site.register(Attendee, AttendeeAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'session', 'intime', 'outtime')
    search_fields = ('attendee__name', 'session__name')
    list_filter = ('session', 'intime', 'outtime')

admin.site.register(Attendance, AttendanceAdmin)