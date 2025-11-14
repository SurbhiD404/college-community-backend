from django.contrib import admin

# Register your models here.
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'sender', 'content', 'timestamp')
    search_fields = ('room_name', 'content', 'sender__email')
    list_filter = ('room_name', 'timestamp')
    ordering = ('-timestamp',)