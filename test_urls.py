import django

if django.VERSION >= (1,10):
    from django.conf.urls import include, url
    patterns = lambda _ignore, x: list([x,])
else:
    from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^messages/', include('messages_extends.urls', namespace='messages')),
)
