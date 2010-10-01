from persistent_messages.models import Message
from persistent_messages.constants import PERSISTENT_MESSAGE_LEVELS
from django.contrib import messages 
from django.contrib.messages.storage.base import BaseStorage
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db.models import Q
import datetime

def get_user(request):
    if hasattr(request, 'user') and request.user.__class__ != AnonymousUser:
        return request.user
    else:
        return AnonymousUser()

"""
Messages need a primary key when being displayed so that they can be closed/marked as read by the user.
Hence, they need to be stored when being added. You can disable this, but then you'll only be able to 
close a message when it is displayed for the second time. 
"""
STORE_WHEN_ADDING = True

#@TODO USE FALLBACK 
class PersistentMessageStorage(FallbackStorage):

    def __init__(self, *args, **kwargs):
        super(PersistentMessageStorage, self).__init__(*args, **kwargs)
        self.non_persistent_messages = []
        self.is_anonymous = not get_user(self.request).is_authenticated()

    def _message_queryset(self, exclude_unread=True):
        qs = Message.objects.filter(user=get_user(self.request)).filter(Q(expires=None) | Q(expires__gt=datetime.datetime.now()))
        if exclude_unread:
            qs = qs.exclude(read=True)
        return qs

    def _get(self, *args, **kwargs):
        """
        Retrieves a list of stored messages. Returns a tuple of the messages
        and a flag indicating whether or not all the messages originally
        intended to be stored in this storage were, in fact, stored and
        retrieved; e.g., ``(messages, all_retrieved)``.
        """
        if not get_user(self.request).is_authenticated():
            return super(PersistentMessageStorage, self)._get(*args, **kwargs)
        messages = []
        for message in self._message_queryset():
            if not message.is_persistent():
                self.non_persistent_messages.append(message)
            messages.append(message)
        return (messages, True)

    def get_persistent(self):
        return self._message_queryset(exclude_unread=False).filter(level__in=PERSISTENT_MESSAGE_LEVELS)

    def get_persistent_unread(self):
        return self._message_queryset(exclude_unread=True).filter(level__in=PERSISTENT_MESSAGE_LEVELS)

    def count_unread(self):
        return self._message_queryset(exclude_unread=True).count()

    def count_persistent_unread(self):
        return self.get_persistent_unread().count()
        
    def _delete_non_persistent(self):
        for message in self.non_persistent_messages:
            message.delete()
        self.non_persistent_messages = []

    def __iter__(self):
        if not get_user(self.request).is_authenticated():
            return super(PersistentMessageStorage, self).__iter__()
        self.used = True
        messages = []
        messages.extend(self._loaded_messages)
        if self._queued_messages:
            messages.extend(self._queued_messages)
        return iter(messages)

    def _prepare_messages(self, messages):
        if not get_user(self.request).is_authenticated():
            return super(PersistentMessageStorage, self)._prepare_messages(messages)
        """
        Obsolete method since model takes care of this.
        """
        pass
        
    def _store(self, messages, response, *args, **kwargs):
        """
        Stores a list of messages, returning a list of any messages which could
        not be stored.

        If STORE_WHEN_ADDING is True, messages are already stored at this time and won't be
        saved again.
        """
        if not get_user(self.request).is_authenticated():
            return super(PersistentMessageStorage, self)._store(messages, response, *args, **kwargs)
        for message in messages:
            if not self.used or message.is_persistent():
                if not message.pk:
                    message.save()
        return []

    def update(self, response):
        if not get_user(self.request).is_authenticated():
            return super(PersistentMessageStorage, self).update(response)
        """
        Deletes all non-persistent, read messages. Saves all unstored messages.
        """
        if self.used:
            self._delete_non_persistent()
        return super(PersistentMessageStorage, self).update(response)

    def add(self, level, message, extra_tags='', subject='', user=None, from_user=None, expires=None, close_timeout=None):
        """
        Queues a message to be stored.

        The message is only queued if it contained something and its level is
        not less than the recording level (``self.level``).
        """
        to_user = user or get_user(self.request)
        if not to_user.is_authenticated():
            if Message(level=level).is_persistent():
                raise NotImplementedError('Persistent message levels cannot be used for anonymous users.')
            else:
                return super(PersistentMessageStorage, self).add(level, message, extra_tags)
        if not message:
            return
        # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return
        # Add the message.
        message = Message(user=to_user, level=level, message=message, extra_tags=extra_tags, subject=subject, from_user=from_user, expires=expires, close_timeout=close_timeout)
        # Messages need a primary key when being displayed so that they can be closed/marked as read by the user.
        # Hence, save it now instead of adding it to queue:
        if STORE_WHEN_ADDING:
            message.save()
        else:
            self.added_new = True
            self._queued_messages.append(message)
