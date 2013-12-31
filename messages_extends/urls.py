# -*- coding: utf-8 -*-
"""urls.py: messages extends"""

from __future__ import unicode_literals

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^mark_read/(?P<message_id>\d+)/$', 'messages_extends.views.message_mark_read', name='message_mark_read'),
    url(r'^mark_read/all/$', 'messages_extends.views.message_mark_all_read', name='message_mark_all_read'),
)
