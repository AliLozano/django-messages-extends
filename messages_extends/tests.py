# -*- coding: utf-8 -*-
"""tests.py: Tests for messages-extends"""

from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage import default_storage
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings

from . import PERSISTENT_MESSAGE_LEVELS, WARNING_PERSISTENT
from .models import Message, MessageRead


class MessagesClient(Client):
    """ Baseline Client for Messages Extends.  This is needed to hook messages into the client
    and assign the user attribute to the request object"""

    def __init__(self, **defaults):
        """Adds messages to the request"""
        super(MessagesClient, self).__init__(**defaults)
        if 'django.contrib.messages' in settings.INSTALLED_APPS:
            self._messages = default_storage(self)

    def login(self, **credentials):
        """This sets the user attibute for a logged in user"""
        if super(MessagesClient, self).login(**credentials):
            self.user = authenticate(**credentials)
            return True
        else:
            self.user = AnonymousUser()
        return False

    def logout(self):
        logout = super(MessagesClient, self).logout()
        if hasattr(self, 'user'):
            self.user = None
        return logout


class MessagesTests(TestCase):
    """Test out homes app"""
    client_class = MessagesClient

    def _get_user(self, username="bob"):
        """Give up a user"""
        user = User.objects.create(username=username)
        user.set_password('password')
        user.save()
        return user

    @override_settings(MESSAGE_LEVEL=1)
    def test_persist_message_levels(self):
        """Test the basic messaging"""
        user =self._get_user()
        self.client.login(username=user.username, password='password')
        for level in PERSISTENT_MESSAGE_LEVELS:
            msg = 'Test {} - {}'.format(level, datetime.datetime.now())
            messages.add_message(self.client, level, msg)
            result = Message.objects.get(level=level)
            self.assertEqual(result.message, msg)
            self.assertEqual(result.user, user)
            self.assertEqual(result.extra_tags, u'')
            self.assertIsNone(result.expires)
            self.assertIsNotNone(result.created)
            self.assertFalse(result.read)

    def test_mark_as_read(self):
        """Test the basic messaging"""
        self.client.login(username=self._get_user().username, password='password')
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning..")
        result = Message.objects.all()[0]
        self.assertFalse(result.read)
        url = reverse('messages:message_mark_read', kwargs={'message_id': result.id})
        self.client.get(url)

        result = Message.objects.all()[0]
        self.assertTrue(result.read)

    def test_for_other_user(self):
        """Test the basic message for another user"""
        self.client.login(username=self._get_user().username, password='password')
        user2 = self._get_user(username="john")

        messages.add_message(self.client, WARNING_PERSISTENT, "Warning..", user=user2)
        result = Message.objects.all()[0]
        self.assertEqual(result.user, user2)

    def test_mark_message_read_for_other_user(self):
        """Test the basic message for another user"""
        self.client.login(username=self._get_user().username, password='password')
        user2 = self._get_user(username="john")
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning..", user=user2)
        result = Message.objects.all()[0]
        self.assertEqual(result.user, user2)
        url = reverse('messages:message_mark_read', kwargs={'message_id': result.id})
        self.client.get(url)
        result = Message.objects.all()[0]
        self.assertFalse(result.read)

    def test_broadcast_message_visible_for_all_users(self):
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning..", user=None)
        user1 = self._get_user()
        user2 = self._get_user(username='john')
        message1 = Message.objects.for_user(user1)[0]
        self.assertEqual(message1.user, None)
        self.assertEqual(message1.message, 'Warning..')
        message2 = Message.objects.for_user(user2)[0]
        self.assertEqual(message1, message2)

    def test_mark_broadcast_message_read(self):
        user = self._get_user()
        self.client.login(username=user.username, password='password')
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning..", user=None)
        message = Message.objects.for_user(user)[0]
        url = reverse('messages:message_mark_read', kwargs={'message_id': message.id})
        self.client.get(url)
        result = Message.objects.for_user(user)
        self.assertEqual(len(result), 0)
        message_read = MessageRead.objects.all()[0]
        self.assertTrue(message_read.message, message)
        self.assertTrue(message_read.user, user)
        self.assertTrue(message_read.read, True)

    def test_broadcast_message_marked_read_still_visible_for_another_user(self):
        user1 = self._get_user()
        user2 = self._get_user(username='john')
        self.client.login(username=user1.username, password='password')
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning..", user=None)
        message1 = Message.objects.for_user(user1)[0]
        message2 = Message.objects.for_user(user2)[0]
        self.assertEqual(message1, message2)
        url = reverse('messages:message_mark_read', kwargs={'message_id': message1.id})
        self.client.get(url)
        result1 = Message.objects.for_user(user1)
        self.assertEqual(len(result1), 0)
        result2 = Message.objects.for_user(user2)
        self.assertEqual(len(result2), 1)

    def test_mark_all_read(self):
        user = self._get_user()
        self.client.login(username=user.username, password='password')
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning1")
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning2")
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning3", user=None)
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning4", user=None)
        user_messages = Message.objects.for_user(user)
        self.assertEqual(len(user_messages), 4)
        url = reverse('messages:message_mark_all_read')
        self.client.get(url)
        result = Message.objects.for_user(user)
        self.assertEqual(len(result), 0)

    def test_add_detail_link(self):
        user = self._get_user()
        self.client.login(username=user.username, password='password')
        messages.add_message(self.client, WARNING_PERSISTENT, "Warning..", user=None, detail_link='http://www.google.com')
        message = Message.objects.for_user(user)[0]
        self.assertEqual(message.detail_link, 'http://www.google.com')
