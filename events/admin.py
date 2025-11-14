from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_time', 'end_time', 'created_by')
    search_fields = ('title', 'description', 'location')
    list_filter = ('start_time', 'end_time', 'created_by')
    ordering = ('-start_time',)

