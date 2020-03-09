# -*- coding: utf-8 -*-
"""urls.py: messages extends"""

from django.conf.urls import url
from messages_extends.views import message_mark_all_read, message_mark_read
urlpatterns = [
    url(r'^mark_read/(?P<message_id>\d+)/$', message_mark_read, name='message_mark_read'),
    url(r'^mark_read/all/$', message_mark_all_read, name='message_mark_all_read'),
]
