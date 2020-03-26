# -*- coding: utf-8 -*-
"""admin.py: messages extends"""

from messages_extends.models import Message
from django.contrib import admin

class MessageAdmin(admin.ModelAdmin):
    list_display = ['level', 'user', 'message', 'created', 'read']

admin.site.register(Message, MessageAdmin)
