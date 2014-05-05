# -*- coding: utf-8 -*-
"""urls.py: messages extends"""

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^mark_read/(?P<message_id>\d+)/$', 'messages_extends.views.message_mark_read', name='message_mark_read'),
    url(r'^mark_read/all/$', 'messages_extends.views.message_mark_all_read', name='message_mark_all_read'),
)
