from django.contrib.messages.api import MessageFailure
from messages_extends.constants import *
from django.contrib import messages

messages.DEFAULT_TAGS.update(DEFAULT_TAGS)

def add_message(request, level, message, extra_tags='', fail_silently=False, *args, **kwargs):
    """
    Attempts to add a message to the request using the 'messages' app.
    """
    if hasattr(request, '_messages'):
        return request._messages.add(level, message, extra_tags, *args, **kwargs)
    if not fail_silently:
        raise MessageFailure('You cannot add messages without installing '
                             'django.contrib.messages.middleware.MessageMiddleware')

messages.add_message = add_message


