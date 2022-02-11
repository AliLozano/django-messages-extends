from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('messages/', include(('messages_extends.urls', 'messages'))),
]
