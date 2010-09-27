import persistent_messages
from persistent_messages.constants import PERSISTENT_MESSAGE_LEVELS
from django.db import models
from django.contrib.auth.models import User 
from django.utils.encoding import force_unicode
from django.contrib import messages
from django.contrib.messages import utils
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

LEVEL_TAGS = utils.get_level_tags()

class Message(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    from_user = models.ForeignKey(User, blank=True, null=True, related_name="from_user")
    subject = models.CharField(max_length=255, blank=True, default='')
    message = models.TextField()
    LEVEL_CHOICES = (
        (messages.DEBUG, 'DEBUG'),
        (messages.INFO, 'INFO'),
        (messages.SUCCESS, 'SUCCESS'),
        (messages.WARNING, 'WARNING'),
        (messages.ERROR, 'ERROR'),
        (persistent_messages.DEBUG, 'PERSISTENT DEBUG'),
        (persistent_messages.INFO, 'PERSISTENT INFO'),
        (persistent_messages.SUCCESS, 'PERSISTENT SUCCESS'),
        (persistent_messages.WARNING, 'PERSISTENT WARNING'),
        (persistent_messages.ERROR, 'PERSISTENT ERROR'),
    )
    level = models.IntegerField(choices=LEVEL_CHOICES)
    extra_tags = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)    
    modified = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    expires = models.DateTimeField(null=True, blank=True)
    close_timeout = models.IntegerField(null=True, blank=True)

    def is_persistent(self):
        return self.level in PERSISTENT_MESSAGE_LEVELS
    is_persistent.boolean = True
    
    def __eq__(self, other):
        return isinstance(other, Message) and self.level == other.level and \
                                              self.message == other.message
    def __unicode__(self):
        if self.subject:
            message = _('%(subject)s: %(message)s') % {'subject': self.subject, 'message': self.message}
        else:
            message = self.message
        return force_unicode(message)

    def _prepare_message(self):
        """
        Prepares the message for saving by forcing the ``message``
        and ``extra_tags`` and ``subject`` to unicode in case they are lazy translations.

        Known "safe" types (None, int, etc.) are not converted (see Django's
        ``force_unicode`` implementation for details).
        """
        self.subject = force_unicode(self.subject, strings_only=True)
        self.message = force_unicode(self.message, strings_only=True)
        self.extra_tags = force_unicode(self.extra_tags, strings_only=True)

    def save(self, *args, **kwargs):
        self._prepare_message()
        super(Message, self).save(*args, **kwargs)

    def _get_tags(self):
        label_tag = force_unicode(LEVEL_TAGS.get(self.level, ''),
                                  strings_only=True)
        extra_tags = force_unicode(self.extra_tags, strings_only=True)
   
        if (self.read):
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
    
