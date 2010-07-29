from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^detail/(?P<message_id>\d+)/$', 'persistent_messages.views.message_detail', name='message_detail'),
    url(r'^mark_read/(?P<message_id>\d+)/$', 'persistent_messages.views.message_mark_read', name='message_mark_read'),
    url(r'^mark_read/all/$', 'persistent_messages.views.message_mark_all_read', name='message_mark_all_read'),
)
