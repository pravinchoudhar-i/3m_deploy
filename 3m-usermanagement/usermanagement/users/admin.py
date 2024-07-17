from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserRegistration)
admin.site.register(Analysis)

class MasterLogAdmin(admin.ModelAdmin):
    model = MasterLog
    list_display = ('timeStamp','description','activity',)
    
admin.site.register(MasterLog, MasterLogAdmin)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

admin.site.register(SMSModule)
admin.site.register(VersionLog)