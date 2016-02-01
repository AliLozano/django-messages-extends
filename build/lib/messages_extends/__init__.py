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


def persistant_debug(request, message, extra_tags='', fail_silently=False, *args, **kwargs):
    """
    Adds a persistant message with the ``DEBUG`` level.
    """
    add_message(request, DEBUG_PERSISTENT, message, extra_tags=extra_tags,
                fail_silently=fail_silently, *args, **kwargs)

messages.persistant_debug = persistant_debug


def persistant_info(request, message, extra_tags='', fail_silently=False, *args, **kwargs):
    """
    Adds a persistant message with the ``INFO`` level.
    """
    add_message(request, INFO_PERSISTENT, message, extra_tags=extra_tags,
                fail_silently=fail_silently, *args, **kwargs)

messages.persistant_info = persistant_info


def persistant_success(request, message, extra_tags='', fail_silently=False, *args, **kwargs):
    """
    Adds a persistant message with the ``SUCCESS`` level.
    """
    add_message(request, SUCCESS_PERSISTENT, message, extra_tags=extra_tags,
                fail_silently=fail_silently, *args, **kwargs)

messages.persistant_success = persistant_success


def persistant_warning(request, message, extra_tags='', fail_silently=False, *args, **kwargs):
    """
    Adds a persistant message with the ``WARNING`` level.
    """
    add_message(request, WARNING_PERSISTENT, message, extra_tags=extra_tags,
                fail_silently=fail_silently, *args, **kwargs)

messages.persistant_warning = persistant_warning


def persistant_error(request, message, extra_tags='', fail_silently=False, *args, **kwargs):
    """
    Adds a persistant message with the ``ERROR`` level.
    """
    add_message(request, ERROR_PERSISTENT, message, extra_tags=extra_tags,
                fail_silently=fail_silently, *args, **kwargs)

messages.persistant_error = persistant_error

