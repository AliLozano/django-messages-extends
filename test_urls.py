import django

if django.VERSION >= (1, 10):
    from django.conf.urls import include, url

    patterns = lambda _ignore, x: list([x, ])
else:
    from django.conf.urls import patterns, include, url

if django.VERSION >= (2, 0):
    urlpatterns = [
        url(r'^messages/', include(('messages_extends.urls', 'messages'))),
    ]
else:
    urlpatterns = patterns('',
                           url(r'^messages/', include('messages_extends.urls', namespace='messages')),
                           )
