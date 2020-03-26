from django.conf.urls import include, url

urlpatterns = [
    url(r'^messages/', include(('messages_extends.urls', 'messages'))),
]
