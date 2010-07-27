from persistent_messages.models import Message
from django.contrib import admin

class MessageAdmin(admin.ModelAdmin):
    list_display = ['level', 'user', 'from_user', 'subject', 'message', 'created', 'read', 'is_persistent']

admin.site.register(Message, MessageAdmin)
