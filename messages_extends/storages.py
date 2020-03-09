# -*- coding: utf-8 -*-
"""storages.py: messages extends"""

from django.utils.module_loading import import_string as get_storage
from django.contrib.messages.storage.base import BaseStorage, Message
from django.conf import settings
from messages_extends.models import Message as PersistentMessage
from messages_extends.constants import PERSISTENT_MESSAGE_LEVELS, STICKY_MESSAGE_LEVELS
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

__author__ = 'ali'

class FallbackStorage(BaseStorage):
    """
    Tries to store all messages in the first backend, storing any unstored
    messages in each subsequent backend backend, by default use
    MESSAGES_STORAGES = ('messages_extends.storages.StickyStorage',
         'messages_extends.storages.PersistentStorage',
         'django.contrib.messages.storage.session.CookieStorage',
         'django.contrib.messages.storage.session.SessionStorage'))
    if you want change the backends, put your custom storages:
    MESSAGES_STORAGES = ('foo.your_storage', 'cookie_storage')
    in your settings
    """

    storages_names = getattr(settings, 'MESSAGES_STORAGES',
        ('messages_extends.storages.StickyStorage',
         'messages_extends.storages.PersistentStorage',
         'django.contrib.messages.storage.cookie.CookieStorage',
         'django.contrib.messages.storage.session.SessionStorage'))

    def __init__(self, *args, **kwargs):
        super(FallbackStorage, self).__init__(*args, **kwargs)

        # get instances of classes of storages_names
        self.storages = [get_storage(storage)(*args, **kwargs)
                         for storage in self.storages_names]

        self._used_storages = set()

    def _get(self, *args, **kwargs):
        """
        Gets a single list of messages from all storage backends.
        """
        all_messages = []
        for storage in self.storages:
            messages, all_retrieved = storage._get()
            # If the backend hasn't been used, no more retrieval is necessary.
            if messages is None:
                break
            if messages:
                self._used_storages.add(storage)
            all_messages.extend(messages)
            # If this storage class contained all the messages, no further
            # retrieval is necessary
            if all_retrieved:
                break
        return all_messages, all_retrieved

    def _store(self, messages, response, *args, **kwargs):
        """
        Stores the messages, returning any unstored messages after trying all
        backends.

        For each storage backend, any messages not stored are passed on to the
        next backend.
        """
        for storage in self.storages:
            if messages:
                messages = storage._store(messages, response,
                    remove_oldest=False)
            # Even if there are no more messages, continue iterating to ensure
            # storages which contained messages are flushed.
            elif storage in self._used_storages:
                storage._store([], response)
                self._used_storages.remove(storage)
        return messages


    def add(self, level, message, extra_tags='', *args, **kwargs):
        """
        Queues a message to be stored.

        The message is only queued if it contained something and its level is
        not less than the recording level (``self.level``).
        """
        if not message:
            return
            # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return
            # Add the message
        self.added_new = True
        message = Message(level, message, extra_tags=extra_tags)
        for storage in self.storages:
            if hasattr(storage, 'process_message'):
                message = storage.process_message(message, *args, **kwargs)
                if not message:
                    return
        self._queued_messages.append(message)

    def _prepare_messages(self, messages):
        """
        Prepares a list of messages for storage.
        """
        for message in messages:
            if hasattr(message, '_prepare'):
                message._prepare()


class PersistentStorage(BaseStorage):
    """
    Save persistent messages in data base
    """

    def __init__(self, request, *args, **kwargs):
        self._sticky_messages = []
        super(PersistentStorage, self).__init__(request, *args, **kwargs)

    def _message_queryset(self, include_read=False):
        """
        Return a queryset of messages for the request user
        """
        expire = timezone.now()


        qs = PersistentMessage.objects.\
        filter(user=self.get_user()).\
        filter(Q(expires=None) | Q(expires__gt=expire))
        if not include_read:
            qs = qs.exclude(read=True)
        return qs


    def _get(self, *args, **kwargs):
        """
        Retrieves a list of stored messages. Returns a tuple of the messages
        and a flag indicating whether or not all the messages originally
        intended to be stored in this storage were, in fact, stored and
        retrieved; e.g., ``(messages, all_retrieved)``.
        """
        is_authenticated = self.get_user().is_authenticated
        if callable(is_authenticated):
            is_authenticated = is_authenticated()
        if is_authenticated is not True:
            return [], False
        return self._message_queryset(), False

    def _store(self, messages, response, *args, **kwargs):
        #There are alredy saved.
        return [message for message in messages if not message.level in PERSISTENT_MESSAGE_LEVELS]

    def process_message(self, message, *args, **kwargs):
        """
        If its level is into persist levels, convert the message to models and save it
        """
        if not message.level in PERSISTENT_MESSAGE_LEVELS:
            return message

        user = kwargs.get("user") or self.get_user()

        try:
            anonymous = user.is_anonymous()
        except TypeError:
            anonymous = user.is_anonymous
        if anonymous:
            raise NotImplementedError('Persistent message levels cannot be used for anonymous users.')
        message_persistent = PersistentMessage()
        message_persistent.level = message.level
        message_persistent.message = message.message
        message_persistent.extra_tags = message.extra_tags
        message_persistent.user = user

        if "expires" in kwargs:
            message_persistent.expires = kwargs["expires"]
        message_persistent.save()
        return None

    def add(self, level, message, extra_tags='', *args, **kwargs):
        """
        Queues a message to be stored.

        The message is only queued if it contained something and its level is
        not less than the recording level (``self.level``).
        """
        if not message:
            return
            # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return
            # Add the message.
        self.added_new = True
        message = Message(level, message, extra_tags=extra_tags)
        message = self.process_message(message, *args, **kwargs)
        if message:
            self._queued_messages.append(message)

    def get_user(self):
        if hasattr(self.request, 'user'):
            return self.request.user
        else:
            return AnonymousUser()


class StickyStorage(BaseStorage):
    """
    Keep messages that are sticky in memory
    """

    def __init__(self, request, *args, **kwargs):
        super(StickyStorage, self).__init__(request, *args, **kwargs)

    def _get(self, *args, **kwargs):
        """
        Retrieves a list of messages from the memory.
        """
        return [], False

    def _store(self, messages, response, *args, **kwargs):
        """
        Delete all messages that are sticky and return the other messages
        This storage never save objects
        """
        return [message for message in messages if not message.level in STICKY_MESSAGE_LEVELS]
