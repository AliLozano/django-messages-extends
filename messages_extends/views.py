# -*- coding: utf-8 -*-
"""views.py: messages extends"""

from __future__ import unicode_literals

from messages_extends.models import Message, MessageRead
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


def message_mark_read(request, message_id):
    if not request.user.is_authenticated():
        raise PermissionDenied
    message = get_object_or_404(Message, pk=message_id)
    if message.user:
        if message.user != request.user:
            raise PermissionDenied
        message.read = True
        message.save()
    else:
        message_read = MessageRead.objects.create(message=message, user=request.user)
        message_read.save()
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse(status=204)


def message_mark_all_read(request):
    if not request.user.is_authenticated():
        raise PermissionDenied
    Message.objects.filter(user=request.user).update(read=True)
    for message in Message.objects.filter(user=None).exclude(messageread__user=request.user):
        MessageRead.objects.create(message=message, user=request.user).save()
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse(status=204)
