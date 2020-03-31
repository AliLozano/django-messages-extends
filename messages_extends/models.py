# -*- coding: utf-8 -*-
"""models.py: messages extends"""

import messages_extends
from django.db import models
from django.utils.encoding import force_text
from django.contrib.messages import utils
from django.conf import settings

LEVEL_TAGS = utils.get_level_tags()

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             on_delete=models.CASCADE)
    message = models.TextField()
    LEVEL_CHOICES = (
        (messages_extends.DEBUG_PERSISTENT, 'PERSISTENT DEBUG'),
        (messages_extends.INFO_PERSISTENT, 'PERSISTENT INFO'),
        (messages_extends.SUCCESS_PERSISTENT, 'PERSISTENT SUCCESS'),
        (messages_extends.WARNING_PERSISTENT, 'PERSISTENT WARNING'),
        (messages_extends.ERROR_PERSISTENT, 'PERSISTENT ERROR'),
        )
    level = models.IntegerField(choices=LEVEL_CHOICES)
    extra_tags = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    expires = models.DateTimeField(null=True, blank=True)

    def __eq__(self, other):
        return isinstance(other, Message) and self.level == other.level and\
               self.message == other.message

    __hash__ = models.Model.__hash__

    def __str__(self):
        return force_text(self.message)

    def _prepare_message(self):
        """
        Prepares the message for saving by forcing the ``message``
        and ``extra_tags`` and ``subject`` to unicode in case they are lazy translations.

        Known "safe" types (None, int, etc.) are not converted (see Django's
        ``force_text`` implementation for details).
        """
        self.message = force_text(self.message, strings_only=True)
        self.extra_tags = force_text(self.extra_tags, strings_only=True)

    def save(self, *args, **kwargs):
        self._prepare_message()
        super(Message, self).save(*args, **kwargs)

    def _get_tags(self):
        label_tag = force_text(LEVEL_TAGS.get(self.level, ''),
            strings_only=True)
        extra_tags = force_text(self.extra_tags, strings_only=True)

        if self.read:
            read_tag = "read"
        else:
            read_tag = "unread"

        if extra_tags and label_tag:
            return u' '.join([extra_tags, label_tag, read_tag])
        elif extra_tags:
            return u' '.join([extra_tags, read_tag])
        elif label_tag:
            return u' '.join([label_tag, read_tag])
        return read_tag

    tags = property(_get_tags)
